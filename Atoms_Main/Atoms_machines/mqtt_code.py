import os
import paho.mqtt.client as mqtt
from django.conf import settings
# from . import multi_topic_file
import ssl
from .Multi_topic_file import *

import time
# from .import io_status_websocket
# ------------------------hive broker----------------------------
import logging

logger = logging.getLogger("django")


def on_connect(client, userdata, flags, reason_code,properties):
    print("in on connect")
    logger.info('hive...on_connect...!')
    logger.info('hive ..on_connect... : %s', reason_code)
    if reason_code==0:
        print('Connected successfully on hive')
        client.subscribe('machine_data_dev')
        client.subscribe('websocket_data_dev')
        client.subscribe('Maithri_test')

    else:
        logger.info('hive ..on_connect...else : %s', reason_code)
        print(f"Connection failed with reason code {reason_code}. Attempting to reconnect...")
        client.reconnect()





def on_message(client, userdata, msg):
    print("in on message")
    logger.info('hive...on_message...!')
    connected_machine_data = msg.payload.decode()  # Assuming the payload is a string
    topic = msg.topic
    if topic == "machine_data_dev":
        all_topics(connected_machine_data,topic)
        from . import io_status_websocket

        io_status_websocket.io_websocket(connected_machine_data)
        io_status_websocket.control_websocket(connected_machine_data)

    if topic == "Maithri_test":
        all_topics(connected_machine_data,topic)
        from . import io_status_websocket

        io_status_websocket.io_websocket(connected_machine_data)
        io_status_websocket.control_websocket(connected_machine_data)

# def on_disconnect(client, userdata, rc):
#     print(f"Disconnected with result code {rc}")
#     # Implement your reconnection logic here
#     print('client.is_connected()',client.is_connected())
#     while not client.is_connected():
#         try:
#             print("Attempting to reconnect...")
#             client.reconnect()
#             time.sleep(1)
#         except Exception as e:
#             print(f"Reconnection failed: {str(e)}")
#             time.sleep(5)





client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
# client.on_disconnect = on_disconnect
client.username_pw_set(settings.MQTT_USER, settings.MQTT_PASSWORD)
client.connect(
   host=settings.MQTT_SERVER,
   port=settings.MQTT_PORT,
   keepalive=settings.MQTT_KEEPALIVE
)
# client.connect(
#    host='broker.hivemq.com',
#    port=1883,
#    keepalive=60
# )
# client.connect("broker.hivemq.com", 1883, 60)


# client.loop_start()

# def mqtt_loop():
#     client.loop_forever()
#
# mqtt_thread = threading.Thread(target=mqtt_loop)
# mqtt_thread.daemon = True
# mqtt_thread.start()


#
# # aws connection  MID004-----------------------------------------------
#
def on_connect_1(client_1, userdata, flags, reason_code,properties):
    print("in on_connect_1")
    logger.info('aws...on_connect...!')
    logger.info('aws ..on_connect... : %s', reason_code)
    if reason_code == 0:
        print('Connected successfully on aws')
        client_1.subscribe('machine_data_dev')
        client_1.subscribe('websocket_data_dev')
        client_1.subscribe('Maithri_test')
        client_1.subscribe('ws_machine_data')
    else:
        logger.info('aws ..on_connect...else : %s', reason_code)
        print(f"Connection failed with reason code {reason_code}. Attempting to reconnect...")
        client_1.reconnect()



# def on_disconnect_1(client_1, userdata, rc):
#     print(f"Disconnected with result code {rc}")
#     # Implement your reconnection logic here
#     while not client_1.is_connected():
#         try:
#             print("Attempting to reconnect...")
#             client_1.reconnect()
#             time.sleep(1)
#         except Exception as e:
#             print(f"Reconnection failed: {str(e)}")
#             time.sleep(5)


def on_message_1(client_1, userdata, msg):
    print("in on_message_1")
    logger.info('aws...on_message...!')


    connected_machine_data = msg.payload.decode()  # Assuming the payload is a string
    # print('connected_machine_data',connected_machine_data)
    topic = msg.topic
    if topic == "machine_data_dev":
        all_topics(connected_machine_data, topic)
        from . import io_status_websocket

        io_status_websocket.io_websocket(connected_machine_data)
        io_status_websocket.control_websocket(connected_machine_data)
    if topic == "Maithri_test":
        all_topics(connected_machine_data,topic)
        from . import io_status_websocket

        io_status_websocket.io_websocket(connected_machine_data)
        io_status_websocket.control_websocket(connected_machine_data)
    if topic == "ws_machine_data":
        from . import io_status_websocket

        io_status_websocket.io_websocket(connected_machine_data)



client_1 = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client_1.on_connect = on_connect_1
client_1.on_message = on_message_1
# client_1.on_disconnect = on_disconnect_1
client_1.username_pw_set(settings.MQTT_USER, settings.MQTT_PASSWORD)
client_1.tls_set(settings.CAPATH, certfile=settings.CERTPATH, keyfile=settings.KEYPATH,
                    cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
client_1.connect(

   host=settings.AWSHOST,
   port=settings.AWSPORT,
   keepalive=settings.MQTT_KEEPALIVE
)

