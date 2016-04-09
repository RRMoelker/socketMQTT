#
# Socket server that forwards messages to (authenticated) MQTT broker
#

import logging
import socket
import sys
from thread import *

import config
from mqtt import MqttConnection

if config.MQTT_AUTHENTICATE:
    import credentials

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

mqttc = MqttConnection()
if config.MQTT_AUTHENTICATE:
    mqttc.connect(credentials.username, credentials.password)
else:
    mqttc.connect()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
logger.info('Socket server created')

try:
    s.bind((config.SOCKET_HOST, config.SOCKET_PORT))
except socket.error as msg:
    logger.critical('Socket bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()
s.listen(10)
logger.info('Socket listening')


def socket_thread(conn):
    conn.send('Welcome to the socketMQTT server.\n')
    while True:
        data = conn.recv(1024)

        logger.info('received: %s', data)

        success = True
        try:
            topic, message = data.split('::')
        except ValueError:
            error_message = 'ERROR, Could not split socket data into topic::message'
            logger.error(error_message)
            reply = error_message
            success = False

        if success:
            logger.info('topic: %s', topic)
            logger.info('message: %s', message)

            success = mqttc.send(topic, message)
            if success:
                reply = 'OK, Message forwarded, topic: ' + topic + ', message: ' + message
            else:
                reply = 'ERROR, could not forward message to MQTT broker'
        conn.send(reply)


# Socket server listens for new connections
while True:
    conn, addr = s.accept()
    logger.info('New connection ' + addr[0] + ':' + str(addr[1]))

    start_new_thread(socket_thread, (conn,))
