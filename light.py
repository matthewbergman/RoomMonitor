from LTR329ALS01 import LTR329ALS01

from sensor import Sensor

class Light(Sensor):
    mqtt_feed1 = "Light1"
    mqtt_feed2 = "Light2"

    def __init__(self, py, mqtt_feed1, mqtt_feed2):
        self.mqtt_feed1 = mqtt_feed1
        self.mqtt_feed2 = mqtt_feed2
        self.light = LTR329ALS01(py)

    def get_data(self, channel):
        light_all = self.light.light()
        var_lux1 = str(light_all[0])
        var_lux2 = str(light_all[1])
        if channel == 0:
            self.logger.debug("LUX 1: "+var_lux1)
            return var_lux1
        else:
            self.logger.debug("LUX 2: "+var_lux2)
            return var_lux2

    def get_mqtt_feed(self, channel):
        if channel == 0:
            return self.mqtt_feed1
        else:
            return self.mqtt_feed2

    def get_channels(self):
        return 2
