"""
MQTT BLE Watchdog will reboot my Raspberry Pi zero if/when BLE shits itself.
"""

import paho.mqtt.client as mqtt
from threading import Timer
from subprocess import run
import logging
import sys

TIMEOUT = 90
TOPIC = "home/TheengsGateway/#"
MQTT_HOST = sys.argv[1]
MQTT_USER = sys.argv[2]
MQTT_PASS = sys.argv[3]


def reboot():
    logging.warning("Restarting Bluetooth and Theengs")
    run("bluetoothctl off".split())
    run("bluetoothctl on".split())
    run("systemctl restart theengs-gateway.service".split())

def on_connect(client, userdata, flags, rc):
    logging.info("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(TOPIC)

def main():
    # Subscribe to a known active MQTT topic.
    # Each time a message arrives, reset a timer.
    # If the timer reaches zero, reboot this computer, BLE has died.

    logging.basicConfig()
    
    client = mqtt.Client("BLE Watchdog")
    client.enable_logger()
    client.username_pw_set(username=MQTT_USER, password=MQTT_PASS)
    client.connect(MQTT_HOST)

    watchdog = Watchdog(timeout=TIMEOUT, handler=reboot)

    def on_message(client, userdata, msg):
        watchdog.reset()

    client.on_message = on_message
    client.on_connect = on_connect
    client.loop_forever()




class Watchdog(Exception):
    def __init__(self, timeout, handler=None):  # timeout in seconds
        self.timeout = timeout
        self.handler = handler if handler is not None else self.defaultHandler
        self.timer = Timer(self.timeout, self.handler)
        self.timer.start()

    def reset(self):
        self.timer.cancel()
        self.timer = Timer(self.timeout, self.handler)
        self.timer.start()

    def stop(self):
        self.timer.cancel()

    def defaultHandler(self):
        raise self


if __name__ == '__main__':
    main()
