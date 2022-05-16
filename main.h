#ifndef MAINHEADER_H
#define MAINHEADER_H

#include <WiFi.h>
#include <PubSubClient.h>
#include <M5stickC.h>

//#define MODEM_SLEEP
//#define LIGHT_SLEEP
//#define DEEP_SLEEP
#define SERIAL_DEBUG_ENABLE

#define BYTES_PER_PACKET_DATA 8 // 8,14 56
#define FIFO_BUFFER_BYTES 952   //
#define MAX_FIFO_SIZE 1008      //
#define REFRESH_SCREEN_FREQ 1   // 1Hz
#define MQTT_BUFFER FIFO_BUFFER_BYTES / BYTES_PER_PACKET_DATA
#define BUFFER_LOOP_SIZE 2
#define WIFI_TIMEOUT_MS 5000

typedef struct status
{
    int lcd_on = 0;
    int wifi_status = 0;
    int mqtt_status = 0;
    float accel[3];
    String fifo_msg = "";
    WiFiClient net;
    PubSubClient client;

}m5Stick_t;

struct MyButton
{
    const uint8_t PIN;
    uint32_t numberKeyPresses;
    bool pressed;
};

void connectToWiFi();
void connectToMQTT();
void WiFiEvent(WiFiEvent_t event);

#endif /* MAINHEADER_H */