import os
import time
import logging

import RPi.GPIO as GPIO

class ObstacleDetector():

    sound_file_path = "./sound-files/{}/{}.mp3"

    def run(self, trigger, echo, language):

        distance = self.get_distance(trigger, echo)
        logging.info("Distance : %.1f" % distance)

        if distance < 100:
            logging.info("You should stop now !")
            self.play_sound_file(self.sound_file_path.format(language, 100))
        elif distance < 200:
            logging.info("The obstacle is 2 meters ahead")
            self.play_sound_file(self.sound_file_path.format(language, 200))
        elif distance < 400:
            logging.info("The obstacle is 4 meters ahead")
            self.play_sound_file(self.sound_file_path.format(language, 400))

    # get distance to the nearest obstacle
    def get_distance(self, trigger, echo):
        # send 10us pulse to trigger
        GPIO.output(trigger, True)
        time.sleep(0.00001)
        GPIO.output(trigger, False)
        start = time.time()
        while GPIO.input(echo) == 0:
            start = time.time()
        while GPIO.input(echo) == 1:
            stop = time.time()
        # calculate pulse length
        duration = stop - start
        # distance = time * speed of sound (cm/s)
        distance = duration * 34000
        # the real distance is the half
        return distance / 2

    def play_sound_file(self, path):
        try:
            os.system("mpg123 {}".format(path))
        except Exception as e:
            logging.error("Error playing sound file {}".format(e.message))