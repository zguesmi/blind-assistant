import time
import os

import RPi.GPIO as GPIO

class ObstacleDetector(object):
    """docstring for ObstacleDetector."""

    def __init__(self, arg):
        super(ObstacleDetector, self).__init__()
        self.arg = arg

    # Get distance between the user and the nearest obstacle
    def get_distance(self, GPIO_TRIGGER, GPIO_ECHO):
        # Send 10us pulse to trigger
        GPIO.output(GPIO_TRIGGER, True)
        time.sleep(0.00001)
        GPIO.output(GPIO_TRIGGER, False)
        start = time.time()
        while GPIO.input(GPIO_ECHO) == 0:
            start = time.time()
        while GPIO.input(GPIO_ECHO) == 1:
            stop = time.time()
        # Calculate pulse length
        duration = stop-start
        # Distance pulse travelled in that time is time
        # multiplied by the speed of sound (cm/s)
        distance = duration * 34000
        # That was the distance there and back so halve the value
        distance = distance / 2
        return distance

    # Play warnings according to distance and language
    def play_sound(self, distance, language):
        os.system("mpg123 resources/sounds/" + language + "/warning" + str(distance) + ".mp3")

    # play warnings
    def warn(self, distance, language):
        try:
            if distance < 100:
                print("you should stop")
                play_sound(100, language)
            elif distance < 200:
                print("The obstacle is 2 meters ahead")
                play_sound(200, language)
            elif distance < 400:
                print("There is an obstacle after 4 meters")
                play_sound(400, language)
        except:
            print("=> Error playing sound")

    def run(self, GPIO_TRIGGER, GPIO_ECHO, language):
        distance = get_distance(GPIO_TRIGGER, GPIO_ECHO)
        print("Distance : %.1f" % distance)
        warn(distance, language)
