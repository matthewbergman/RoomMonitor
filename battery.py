from sensor import Sensor

class Battery(Sensor):
    mqtt_feed = "volts"
    py = None

    def __init__(self, py, mqtt_feed):
        self.mqtt_feed = mqtt_feed
        self.py = py

    def get_data(self, channel):
        var_volt = str(self.py.read_battery_voltage())
        self.logger.debug("V: "+var_volt)
        return var_volt
