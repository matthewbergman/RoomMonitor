import logging

class Sensor:
    mqtt_feed = "sensor"
    logger = logging.getLogger(__name__)

    def get_data(self, channel):
        return ""

    def get_mqtt_feed(self, channel):
        return self.mqtt_feed

    def get_channels(self):
        return 1
