import logging
import time

from network import LTE
import pycom

from commanager import CommManager
import config

class LTEManager(CommManager):
    logger = logging.getLogger(__name__)
    lte = LTE()

    def isconnected(self):
        return self.lte.isconnected()

    def scan(self):
        return True

    def connect(self):
        attempts = 0

        if not self.lte_attach():
            print("LTE attach failed")
            return False

        while not self.lte.isconnected():
            print("Connecting to LTE, attempt "+str(attempts)+"/3")
            if self.lte_connect_attempt():
                break
            if attempts < 3:
                attempts += 1
            else:
                break
        if self.lte.isconnected():
            print("Connected to LTE\n")
            pycom.rgbled(0x0000FF)
            return True
        return False

    def lte_connect_attempt(self):
        counter = 0
        self.lte.connect()
        while not self.lte.isconnected():
            time.sleep(1)
            counter += 1
            if counter == 5:
                return False
        return True

    def lte_attach(self):
        counter = 0
        print("Attaching to LTE")
        self.lte.attach()
        while not self.lte.isattached():
            time.sleep(1)
            counter += 1
            if counter == 15:
                return False
        return True

    def disconnect(self):
        if self.lte.isconnected():
            self.lte.disconnect()
        if self.lte.isattached():
            self.lte.dettach()
        return True
