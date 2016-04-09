import logging
import paho.mqtt.client as mqtt

import config

logger = logging.getLogger(__name__)


def on_connect(client, userdata, rc):
    """
    The callback for when the client receives a CONNACK response from the server.
    Subscribing in on_connect() means that if we lose the connection and
    reconnect then subscriptions will be renewed.
    """
    logger.info("Connected with result code %s", str(rc))
    client.subscribe("$SYS/#")


class MqttConnection:
    def connect(self, user=None, password=None):
        self.mqttc = mqtt.Client()
        self.mqttc.on_connect = on_connect
        if config.MQTT_AUTHENTICATE:
            self.mqttc.username_pw_set(user, password)
        self.mqttc.connect(config.MQTT_HOST, config.MQTT_PORT, 60)
        logger.info('MQTT connect called, waiting for connected')
        self.mqttc.loop_start()
        logger.info('MQTT looping in other thread')

    def send(self, topic, message):
        logger.debug('MQTT sending message %s', message)
        (result, mid) = self.mqttc.publish(topic, message)
        if result == mqtt.MQTT_ERR_SUCCESS:
            logger.info('MQTT message send')
            return True
        elif result == mqtt.MQTT_ERR_NO_CONN:
            logger.critical('ERROR, MQTT message not send, client not connected')
            return False
