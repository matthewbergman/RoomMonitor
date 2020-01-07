from MPL3115A2 import MPL3115A2

from sensor import Sensor

class Pressure(Sensor):
    mqtt_feed = "pressure"

    def __init__(self, py, mqtt_feed):
        self.mqtt_feed = mqtt_feed
        self.press = MPL3115A2(py)

    def get_data(self, channel):
        var_press = str(self.press.pressure())
        self.logger.debug("Pressure: "+var_press)
        return var_press
