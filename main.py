# main.py
#
# Matt Bergman
# Copyright (C) 2018
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys
import time
import logging

import pycom
from pysense import Pysense
from machine import SD

from comms import Comms
from datamanager import DataManager
from accelerometer import Accelerometer
from light import Light
from pressure import Pressure
from temphum import TempHum
from battery import Battery
from wifimanager import WiFiManager
import config

pycom.heartbeat(False) # disable the blue blinking

py = Pysense()
sd = SD()
os.mount(sd, '/sd')
csv_file = open('/sd/data.csv', 'a')
log_file = open("/sd/log.txt", 'a')

logging.basicConfig(level=logging.DEBUG, filename=log_file)
logger = logging.getLogger("RoomMonitor")
logger.debug("Main loop starting")

comms = Comms()
wifi = WiFiManager()
comms.add_manager(0,wifi)

manager = DataManager(csv_file=csv_file)
acc = Accelerometer(py, config.manager_mqtt_user+"/feeds/"+config.manager_mqtt_name+".acceleration")
manager.add_sensor(acc)
light = Light(py, config.manager_mqtt_user+"/feeds/"+config.manager_mqtt_name+".light-1", config.manager_mqtt_user+"/feeds/"+config.manager_mqtt_name+".light-2")
manager.add_sensor(light)
press = Pressure(py, config.manager_mqtt_user+"/feeds/"+config.manager_mqtt_name+".pressure")
manager.add_sensor(press)
temphum = TempHum(py, config.manager_mqtt_user+"/feeds/"+config.manager_mqtt_name+".temperature", config.manager_mqtt_user+"/feeds/"+config.manager_mqtt_name+".humidity")
manager.add_sensor(temphum)
batt = Battery(py, config.manager_mqtt_user+"/feeds/"+config.manager_mqtt_name+".voltage")
manager.add_sensor(batt)

try:
    if not comms.connect():
        comms.disconnect()
        pycom.rgbled(0x0000FF)
        time.sleep(2)
    if not manager.send_data(comms.get_active_manager()):
        comms.disconnect()
        pycom.rgbled(0xFF00FF)
        time.sleep(2)
except KeyboardInterrupt:
    manager.disconnect()
    comms.disconnect()
    csv_file.close()
    log_file.close()
    try:
        sys.exit(0)
    except:
        pass
except Exception as e:
    pycom.rgbled(0x00FFFF)
    logger.exception('Main loop exception')

csv_file.close()
log_file.close()
time.sleep(5)
pycom.rgbled(0x000000)


py.setup_int_pin_wake_up(False)
py.setup_sleep(300)
py.go_to_sleep()
