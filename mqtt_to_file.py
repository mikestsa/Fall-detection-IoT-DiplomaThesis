#!/usr/bin/env python

import sys
import time

from commlib.msg import PubSubMessage, MessageHeader, DataClass
from commlib.node import Node, TransportType
from commlib.transports.mqtt import ConnectionParameters
import json
import redis

from datetime import datetime

r = redis.Redis(
    host = 'localhost',
    port = '6379')

f = open("mqtt_data.txt", "w")

@DataClass
class SonarMessage(PubSubMessage):
    accel: [float]


def on_message(msg):
    list_mqtt_accel = msg["accel"]
    for list_value in list_mqtt_accel:
        value = json.dumps(list_value)
        # print(value.strip('[]'))
        f.write(value.strip('[]'))
        f.write("\n")
    dateTimeObj = datetime.now()
    print(dateTimeObj)
    print(len(list_mqtt_accel))

def mqtt_to_file():
    node = Node(node_name='obstacle_avoidance_node',
                transport_type=TransportType.MQTT,
                connection_params=ConnectionParameters(),
                # heartbeat_uri='nodes.add_two_ints.heartbeat',
                debug=True)

    node.create_subscriber(topic='M5stick/accel',
                           on_message=on_message)

    node.run_forever(sleep_rate=1)



if __name__ == '__main__':
    mqtt_to_file()
