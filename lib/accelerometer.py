import math

from LIS2HH12 import LIS2HH12

from sensor import Sensor

class Accelerometer(Sensor):
    mqtt_feed = "acceleration"

    def __init__(self, py, mqtt_feed):
        self.mqtt_feed = mqtt_feed
        self.acc = LIS2HH12(py)

    def get_data(self, channel):
        acc_all = self.acc.acceleration()
        acc_vector = math.sqrt((acc_all[0]*acc_all[0])+(acc_all[1]*acc_all[1])+(acc_all[2]*acc_all[2]))
        var_acc = str(acc_vector)
        self.logger.debug("ACC: "+var_acc)
        return var_acc

    def enable_activity_interrupt(self, severity, duration):
        self.acc.enable_activity_interrupt(severity, duration)
