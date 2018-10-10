import os
import time
import logging

import RPi.GPIO as GPIO

from obstacle_detector import ObstacleDetector
from document_reader import DocumentReader


class Config():

    def __init__(self):
        LANG = "EN"
        GPIO_TRIGGER = 23
        GPIO_ECHO = 24
        GPIO_CHANGE_MODE_BUTTON = 16
        GPIO_CAPTURE_IMAGE_BUTTON = 25
        LOGFILE = '/tmp/blind-assistant.log'
        LOGLEVEL = logging.INFO


class Main():

    config = None

    def __init__(self, config):
        config = Config()
        self.setup()

    def setup(self):
        # set logging file and level
        logging.basicConfig(filename=self.config.LOGFILE, level=self.config.LOGLEVEL)

        # Use BCM GPIO references instead of physical pin numbers
        GPIO.setmode(GPIO.BCM)

        # Set pins as output and input
        GPIO.setup(self.config.GPIO_TRIGGER, GPIO.OUT)  # Trigger
        GPIO.setup(self.config.GPIO_ECHO, GPIO.IN)      # Echo

        # Set trigger to False (Low)
        GPIO.output(self.config.GPIO_TRIGGER, False)

        GPIO.setup(self.config.GPIO_CHANGE_MODE_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.config.GPIO_CAPTURE_IMAGE_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # Allow module to settle
        time.sleep(0.1)

        GPIO.add_event_detect(self.config.GPIO_CHANGE_MODE_BUTTON, GPIO.BOTH)
        GPIO.add_event_detect(self.config.GPIO_CAPTURE_IMAGE_BUTTON, GPIO.FALLING)

        # increase sound volume
        os.system("amixer set PCM -- 100%")

    def run(self):

        logging.info('Started')
        obstacle_detector = ObstacleDetector()
        document_reader = DocumentReader()

        while True:
            logging.info("Running obstacle detector")
            obstacle_detector.run(self.config.GPIO_TRIGGER, self.config.GPIO_ECHO, self.config.LANG)

            if GPIO.event_detected(self.config.GPIO_CHANGE_MODE_BUTTON) and GPIO.input(self.config.GPIO_CHANGE_MODE_BUTTON) == False:
                logging.info("Running document reader")

                while True:
                    if GPIO.event_detected(self.config.GPIO_CAPTURE_IMAGE_BUTTON):
                        document_reader.run()
                        # camera_mode(camera) maybe u should use one camera instance
                    elif GPIO.event_detected(self.config.GPIO_CHANGE_MODE_BUTTON) and GPIO.input(self.config.GPIO_CHANGE_MODE_BUTTON) == True:
                        break

            time.sleep(0.1)

        logging.info('Finished')

if __name__ == '__main__':
    pass