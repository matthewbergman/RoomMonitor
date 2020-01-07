import math
import time
import sys
import logging

import pycom
from mqtt import MQTTClient

import config

class DataManager():
    machine_name = "ME"
    mqtt_server = "SERVER"
    mqtt_user = "USER"
    mqtt_password = "PASSWORD"
    interval = 60
    mqtt_port = 1883
    client = None
    sensors = []
    logger = logging.getLogger(__name__)
    csv_file = None

    def __init__(self, csv_file=None):
        if csv_file != None:
            self.csv_file = csv_file

        try:
            self.machine_name = config.manager_machine_name
        except:
            pass
        try:
            self.mqtt_server = config.manager_mqtt_server
        except:
            pass
        try:
            self.mqtt_user = config.manager_mqtt_user
        except:
            pass
        try:
            self.mqtt_password = config.manager_mqtt_password
        except:
            pass
        try:
            self.mqtt_port = config.manager_mqtt_port
        except:
            pass
        try:
            self.interval = config.manager_interval
        except:
            pass

    def add_sensor(self, sensor):
        self.sensors.append(sensor)

    def send_data(self, color):
        self.logger.debug(self.machine_name+" "+self.mqtt_server+" "+self.mqtt_user+" "+self.mqtt_password+" "+str(self.mqtt_port))
        self.client = MQTTClient(self.machine_name, self.mqtt_server, user=self.mqtt_user, password=self.mqtt_password, port=self.mqtt_port)
        self.client.connect()

        try:
            while True:
                if color == 0:
                    pycom.rgbled(0x00FF00)
                else:
                    pycom.rgbled(0x0000FF)

                for sensor in self.sensors:
                    for channel in range(sensor.get_channels()):
                        data = sensor.get_data(channel)
                        self.client.publish(topic=sensor.get_mqtt_feed(channel), msg=data)
                        time.sleep(0.2)
                        self.csv_file.write(data+",")
                self.csv_file.write("\r\n")

                pycom.rgbled(0x000000)

                #client.check_msg()
                if self.interval == 0:
                    self.client.disconnect()
                    break

                time.sleep(self.interval)
        except KeyboardInterrupt:
            try:
                sys.exit(0)
            except:
                return False
        except Exception as exc:
            self.logger.exception('send_data')
            return False

        return True

    def sub_cb(self, topic, msg):
       self.logger.debug(topic+": "+msg)
