import time
import sys
import logging

import pycom
import config

class Comms:
    managers = {}
    logger = logging.getLogger(__name__)
    active_manager = None

    def add_manager(self, index, manager):
        self.managers[index] = manager

    def connect(self):
        if self.isConnected():
            return True

        pycom.rgbled(0xFF0000)
        try:
            for index in range(len(self.managers)):
                if self.managers[index].connect():
                    self.active_manager = index
                    if index == 0:
                        pycom.rgbled(0x00FF00)
                    else:
                        pycom.rgbled(0x0000FF)
                    return True
        except KeyboardInterrupt:
            try:
                sys.exit(0)
            except:
                return False
        except Exception as exc:
            self.logger.exception('connect')
        return False

    def get_active_manager(self):
        return self.active_manager

    def isConnected(self):
        try:
            for index in range(len(self.managers)):
                if self.managers[index].isconnected():
                    return True
        except Exception as exc:
            self.logger.exception('isconnected')
        return False

    def disconnect(self):
        try:
            for index in range(len(self.managers)):
                if self.managers[index].disconnect():
                    return True
            return True
        except Exception as exc:
            self.logger.exception('disconnect')
        return False
