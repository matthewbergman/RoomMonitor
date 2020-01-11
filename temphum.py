from SI7006A20 import SI7006A20

from sensor import Sensor

class TempHum(Sensor):
    mqtt_feed1 = "Temperature"
    mqtt_feed2 = "Humidity"

    def __init__(self, py, mqtt_feed1, mqtt_feed2):
        self.mqtt_feed1 = mqtt_feed1
        self.mqtt_feed2 = mqtt_feed2
        self.temp = SI7006A20(py)

    def get_data(self, channel):
        var_temp = str(self.temp.temperature())
        var_hum = str(self.temp.humidity())
        if channel == 0:
            self.logger.debug("TEMP: "+var_temp)
            return var_temp
        else:
            self.logger.debug("HUM: "+var_hum)
            return var_hum

    def get_mqtt_feed(self, channel):
        if channel == 0:
            return self.mqtt_feed1
        else:
            return self.mqtt_feed2

    def get_channels(self):
        return 2
