import logging

class CommManager:
    logger = logging.getLogger(__name__)

    def isconnected(self):
        return False

    def scan(self):
        return False

    def connect(self):
        return False

    def disconnect(self):
        return False
