# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information.

import paho.mqtt.client as mqtt
import random
import time
import sys

# Using the Python Device SDK for IoT Hub:
#   https://github.com/Azure/azure-iot-sdk-python
# The sample connects to a device-specific MQTT endpoint on your IoT Hub.
import iothub_client
# pylint: disable=E0611
from iothub_client import IoTHubClient, IoTHubClientError, IoTHubTransportProvider, IoTHubClientResult
from iothub_client import IoTHubMessage, IoTHubMessageDispositionResult, IoTHubError, DeviceMethodReturnValue

# The device connection string to authenticate the device with your IoT hub.
# Using the Azure CLI:
# az iot hub device-identity show-connection-string --hub-name {YourIoTHubName} --device-id MyNodeDevice --output table
CONNECTION_STRING = "HostName=akiothubtest.azure-devices.net;DeviceId=phone;SharedAccessKey=C6Bah8RPI8fg95jVohJ9yx4WKzZkmgsS9xah4lISFok="

# Using the MQTT protocol.
PROTOCOL = IoTHubTransportProvider.MQTT
MESSAGE_TIMEOUT = 10000

# Define the JSON message to send to IoT Hub.
TEMPERATURE = 20.0
HUMIDITY = 60
MSG_TXT = "{\"temperature\": %.2f,\"humidity\": %.2f}"

def send_confirmation_callback(message, result, user_context):
    print ( "IoT Hub responded to message with status: %s" % (result) )

def iothub_client_init():
    # Create an IoT Hub client
    client = IoTHubClient(CONNECTION_STRING, PROTOCOL)
    return client

def on_log(client, userdata, level, buf):
    print("log: " + str(buf))
    
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connection successful")
    else:
        print("Bad connection. Returned code: ", rc)
        
def on_disconnect(client, userdata, flags, rc = 0):
    print("Disconnect result code: " + str(rc))

data = ''
def on_message(client, userdata, msg):
    
    global data
    topic = msg.topic
    m_decode = str(msg.payload.decode("utf-8", "ignore"))
    msg_out = "Message received: ", topic, ' ', m_decode
    data = m_decode
    
    
    
broker = "192.168.1.37"
m_client = mqtt.Client("1")
#m_client = mqtt.Client()

m_client.on_connect = on_connect
m_client.on_disconnect = on_disconnect
#client.on_log = on_log
m_client.on_message = on_message
m_client.username_pw_set("")

print("Connecting to borker: ", broker)

m_client.connect(broker)
m_client.loop_start()

def iothub_client_telemetry_sample_run():
    global data
    try:
        client = iothub_client_init()
        print ( "IoT Hub device sending periodic messages, press Ctrl-C to exit" )

        while True:
#             m_client.subscribe("sensornode/live/Gyroscope/z")    
            m_client.subscribe("sensornode/livestream/Accelerometer/z") #Your MQTT topic
#             m_client.subscribe("sensornode/live/Accelerometer/x")
            print(data)
            
            # Build the message with simulated telemetry values.
            temperature = TEMPERATURE + (random.random() * 15)
            humidity = HUMIDITY + (random.random() * 20)
            msg_txt_formatted = MSG_TXT % (temperature, humidity)
            message = IoTHubMessage(data)

            # Add a custom application property to the message.
            # An IoT hub can filter on these properties without access to the message body.
#             prop_map = message.properties()
#             if temperature > 30:
#               prop_map.add("temperatureAlert", "true")
#             else:
#               prop_map.add("temperatureAlert", "false")

            # Send the message.
            #print( "Sending message: %s" % message.get_string() )
            client.send_event_async(message, send_confirmation_callback, None)
            time.sleep(1)

    except IoTHubError as iothub_error:
        print ( "Unexpected error %s from IoTHub" % iothub_error )
        return
    except KeyboardInterrupt:
        print ( "IoTHubClient sample stopped" )

if __name__ == '__main__':
    print ( "IoT Hub Quickstart #1 - Simulated device" )
    print ( "Press Ctrl-C to exit" )
    iothub_client_telemetry_sample_run() 
