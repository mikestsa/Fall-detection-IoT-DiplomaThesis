#include "main.h"
#include "lcd_update.h"

m5Stick_t m5Stick;

const char ssid[] = "m5stack";
const char pass[] = "m5stackc";
const char *mqtt_server = "192.168.2.10";

float lastPower;
unsigned long previous_refresh = 0;
volatile bool read_fifo = false;

uint8_t DataBuff[MAX_FIFO_SIZE];
float accelData[3];

WiFiClient net;
PubSubClient client(mqtt_server,1883,net);
SemaphoreHandle_t sema_MQTT_KeepAlive;

int sent = 0;
pthread_t threadId;
String packet[BUFFER_LOOP_SIZE];

MyButton button1 = {18, 0, false};

/*
    Important to not set vTaskDelay to less then 10. Errors begin to develop with the MQTT and network connection.
    makes the initial wifi/mqtt connection and works to keeps those connections open.
*/
void MQTTkeepalive(void *pvParameters)
{
  // setting must be set before a mqtt connection is made
  client.setKeepAlive(90); // setting keep alive to 90 seconds makes for a very reliable connection, must be set before the 1st connection is made.
  for (;;)
  {
    // check for a is-connected and if the WiFi 'thinks' its connected, found checking on both is more realible than just a single check
    if ((client.connected()) && (WiFi.status() == WL_CONNECTED))
    {
      xSemaphoreTake(sema_MQTT_KeepAlive, portMAX_DELAY); // whiles MQTTlient.loop() is running no other mqtt operations should be in process
      client.loop();
      xSemaphoreGive(sema_MQTT_KeepAlive);
    }
    else
    {
      Serial.print("MQTT keep alive found MQTT status ");
      Serial.print(String(client.connected())); 
      Serial.print("WiFi status");
      Serial.println(String(WiFi.status()));
      if (!(WiFi.status() == WL_CONNECTED))
      {
        connectToWiFi();
      }
      connectToMQTT();
    }
    vTaskDelay(250); // task runs approx every 250 mS
  }
  vTaskDelete(NULL);
}
////
void connectToMQTT()
{
  // create client ID from mac address
  String clientID = String("ESP") + String("-M5stick");
  Serial.print("connect to mqtt as client ");
  Serial.println(clientID);
  while (!client.connected())
  {
    if (!(WiFi.status() == WL_CONNECTED))
    {
      connectToWiFi();
    }
    client.connect(clientID.c_str());
    Serial.println("connecting to MQTT");
    vTaskDelay(250);
  }
  Serial.println("MQTT Connected");
}
//
void connectToWiFi()
{
  Serial.println("connect to wifi");
  while (WiFi.status() != WL_CONNECTED)
  {
    WiFi.disconnect();
    WiFi.begin(ssid, pass);
    Serial.println(" waiting on wifi connection");
    Serial.print("WiFi status: ");
    Serial.println(WiFi.status());
    vTaskDelay(1000);
  }
  Serial.println("Connected to WiFi");
  WiFi.onEvent(WiFiEvent);
}
////
void WiFiEvent(WiFiEvent_t event)
{
  switch (event)
  {
  case SYSTEM_EVENT_STA_CONNECTED:
    Serial.println("Connected to access point");
    break;
  case SYSTEM_EVENT_STA_DISCONNECTED:
    Serial.println("Disconnected from WiFi access point");
    break;
  case SYSTEM_EVENT_AP_STADISCONNECTED:
    Serial.println("WiFi client disconnected");
    break;
  default:
    break;
  }
}

void setup_wifi()
{
  WiFi.enableSTA(true);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, pass);
  delay(10);

  while (WiFi.waitForConnectResult() != WL_CONNECTED)
  {
    delay(100);
    #ifdef SERIAL_DEBUG_ENABLE
      Serial.printf("Status wifi :%d\n", WiFi.waitForConnectResult());
    #endif
  }
  randomSeed(micros());
}

void reconnect()
{
  // Loop until we're reconnected
  uint8_t numOftry = 0;
  if (!(WiFi.status() == WL_CONNECTED))
  {
    WiFi.disconnect();
    setup_wifi();
  }

  while (!client.connected())
  {
    String clientId = "ESP8266Client-";
    clientId += String(random(0xffff), HEX);

#ifdef SERIAL_DEBUG_ENABLE
    Serial.print("Attempting MQTT connection...");
#endif
    // Attempt to connect
    if (client.connect(clientId.c_str()))
    {
#ifdef SERIAL_DEBUG_ENABLE
      Serial.println("connected");
#endif
      client.publish("/M5stick/Init", "hello world");
      numOftry = 0;
    }
    else
    {
#ifdef SERIAL_DEBUG_ENABLE
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
#endif
      // Wait 5 seconds before retrying
      delay(10);
      if (numOftry++ > 500)
        esp_restart();
    }
  }

}

void IRAM_ATTR isr()
{
  button1.numberKeyPresses += 1;
  button1.pressed = true;
}

void IRAM_ATTR fifo_get_data()
{
    read_fifo++;
}

TaskHandle_t xHandle;
void setup()
{
  M5.begin();
  M5.Axp.begin(); // Serial for debug

#ifdef SERIAL_DEBUG_ENABLE
  Serial.begin(115200);
#endif
  
  attachInterrupt(BUTTON_A_PIN, isr, FALLING);

  // MPU6886 SETUP
  pinMode(GPIO_NUM_35, INPUT);
  attachInterrupt(GPIO_NUM_35, fifo_get_data, RISING);
  M5.Mpu6886.Init();
  M5.Mpu6886.setFIFOEnable(true);
  M5.Mpu6886.setFIFOWmTHS(FIFO_BUFFER_BYTES);
  M5.Mpu6886.getFIFOWmStatus();
  
  //esp_reset_reason_t rst_info = esp_reset_reason();

  if(!client.setBufferSize(2500)){
#ifdef SERIAL_DEBUG_ENABLE
    Serial.println("Unable to resize MQTT Buffer");
#endif
  }

  sema_MQTT_KeepAlive = xSemaphoreCreateBinary();
  xSemaphoreGive( sema_MQTT_KeepAlive ); // found keep alive can mess with a publish, stop keep alive during publish

  xTaskCreatePinnedToCore(MQTTkeepalive, "MQTTkeepalive", 20000, NULL, 3, &xHandle, 1);

#ifdef LIGHT_SLEEP
  esp_sleep_enable_ext0_wakeup(GPIO_NUM_35, 1);
  delay(10);
  #endif

}



void loop()
{

  if (M5.Mpu6886.getFIFOWmStatus() && read_fifo)
  {
    read_fifo = 0;


    if (M5.Mpu6886.ReadFIFOCount() >= FIFO_BUFFER_BYTES)
    {
      Serial.print("Read Buffer to packect: ");
      Serial.println(sent);
      //vTaskResume(xHandle);
      //Serial.println(WiFi.status());
      //Serial.println(client.state());
      m5Stick.fifo_msg = String(M5.Mpu6886.ReadFIFOCount());
      M5.Mpu6886.ReadFIFOBuff(DataBuff, FIFO_BUFFER_BYTES);

      packet[sent] = "{\"accel\":[";

      
      for (size_t i = 0, j = 0; i < FIFO_BUFFER_BYTES; i += BYTES_PER_PACKET_DATA, j++)
      {
        accelData[0] = (int16_t)(((int16_t)DataBuff[i] << 8) | DataBuff[i + 1]) * M5.Mpu6886.aRes;
        accelData[1] = (int16_t)(((int16_t)DataBuff[i + 2] << 8) | DataBuff[i + 3]) * M5.Mpu6886.aRes;
        accelData[2] = (int16_t)(((int16_t)DataBuff[i + 4] << 8) | DataBuff[i + 5]) * M5.Mpu6886.aRes;
        packet[sent] += String("[" + String(accelData[0]) + "," + String(accelData[1]) + "," + String(accelData[2]) + "," + String(button1.pressed) + "]");
        packet[sent] += i + BYTES_PER_PACKET_DATA >= FIFO_BUFFER_BYTES ? "]}" : ",";
      }
      
      //Serial.println(packet[sent]);

      button1.pressed = false;

      if (sent == BUFFER_LOOP_SIZE-1)
      {
        vTaskResume(xHandle);
        Serial.println("Packet are ready");
        while (!client.connected())
        {
          delay(250);
        }

          xSemaphoreTake(sema_MQTT_KeepAlive, portMAX_DELAY);
          if (client.connected())
          {
            Serial.println("Sent packets ");
            for (size_t i = 0; i < BUFFER_LOOP_SIZE; i++)
            {
              
              if (!client.publish("M5stick/accel", packet[i].c_str()))
              {
                delay(5);
              #ifdef SERIAL_DEBUG_ENABLE
                Serial.printf("NOT publish :%d \n", client.state());
              #endif
                m5Stick.fifo_msg = "NOT Published" + String(client.state());
              }else{
                #ifdef SERIAL_DEBUG_ENABLE
                Serial.printf("Pacekt publish : ok \n");
                // Serial.println(packet[i]);
                #endif
                m5Stick.fifo_msg = "Published" + String(client.state());
              }

              delay(5);
            }
            Serial.println("Sent packets complete ");
            float power = M5.Axp.GetBatVoltage() * M5.Axp.GetBatCurrent();
            lastPower = M5.Axp.GetPowerbatData();
            client.publish("M5stick/power", String(lastPower).c_str());
          }
          xSemaphoreGive(sema_MQTT_KeepAlive);
          vTaskSuspend(xHandle);
      }

#ifdef SERIAL_DEBUG_ENABLE
        Serial.print("Data sent is :");
        Serial.println(sent);
      #endif

      sent = (++sent) % BUFFER_LOOP_SIZE;

      
    }

#ifdef MODEM_SLEEP
    WiFi.setSleep(WIFI_PS_MIN_MODEM);
    //setCpuFrequencyMhz(80)
#endif

    Serial.println("Wifi Disconnect ");
    WiFi.disconnect();
    while (WiFi.status() == WL_CONNECTED)
    {
  #ifdef SERIAL_DEBUG_ENABLE
      Serial.printf("WiFi disconnect status: %d\n", WiFi.status());
  #endif
      delay(1);
    }

    delay(500);


#ifdef LIGHT_SLEEP
    // M5.Axp.ScreenBreath(0);

    
    M5.Axp.SetLDO2(false);
    esp_light_sleep_start();
    M5.Axp.SetLDO2(true);
    // M5.Axp.ScreenBreath(9);
#endif

  }

  if (millis() - previous_refresh >= REFRESH_SCREEN_FREQ * 1000)
  {
    M5.Mpu6886.getAccelData(&m5Stick.accel[0], &m5Stick.accel[1], &m5Stick.accel[2]);
    lcd_update(&m5Stick);
    previous_refresh = millis();
  }

delay(10);

}