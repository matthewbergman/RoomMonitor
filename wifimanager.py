import logging
import time

from network import WLAN
import pycom

from commanager import CommManager
import config

class WiFiManager(CommManager):
    logger = logging.getLogger(__name__)
    wlan = WLAN(mode=WLAN.STA)
    ssid = "MYSSID"
    password = "MYPASS"

    def __init__(self):
        try:
            self.ssid = config.comms_ssid
        except:
            pass
        try:
            self.password = config.comms_password
        except:
            pass

    def isconnected(self):
        return self.wlan.isconnected()

    def scan(self):
        nets = self.wlan.scan()
        for net in nets:
            if net.ssid == self.ssid:
                self.logger.debug("SSID found: "+self.ssid)
                return True
        self.logger.debug("SSID NOT found: "+self.ssid)
        return False

    def connect(self):
        attempts = 0

        if not self.scan():
            return False

        while not self.wlan.isconnected():
            self.logger.debug("Connecting to wifi, attempt "+str(attempts)+"/3")
            if self.wifi_connect_attempt():
                break
            if attempts < 3:
                attempts += 1
            else:
                break
        if self.wlan.isconnected():
            self.logger.debug("Connected to Wifi\n")
            pycom.rgbled(0x00FF00)
            return True
        return False

    def wifi_connect_attempt(self):
        counter = 0
        self.wlan.connect(self.ssid, auth=(WLAN.WPA2, self.password), timeout=5000)
        while not self.wlan.isconnected():
            time.sleep(1)
            counter += 1
            if counter == 5:
                return False
        return True

    def disconnect(self):
        if self.wlan.isconnected():
            self.wlan.disconnect()
        return True
