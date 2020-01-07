from L76GNSS import L76GNSS

from sensor import Sensor

class GPS(Sensor):
    mqtt_feed1 = "Lat"
    mqtt_feed2 = "Lon"

    def __init__(self, py, mqtt_feed1, mqtt_feed2):
        self.mqtt_feed1 = mqtt_feed1
        self.mqtt_feed2 = mqtt_feed2
        self.light = L76GNSS(py, timeout=1)

    def get_data(self, channel):
        var_coords = self.gps.coordinates()
        var_lat = ""
        var_lon = ""
        if var_coords[0] != None:
            var_lat = str(var_coords[0])
            var_lon = str(var_coords[1])

        if channel == 0:
            self.logger.debug("LAT: "+var_lat)
            return var_lat
        else:
            self.logger.debug("LON: "+var_lon)
            return var_lon

    def get_mqtt_feed(self, channel):
        if channel == 0:
            return self.mqtt_feed1
        else:
            return self.mqtt_feed2

    def get_channels(self):
        return 2
