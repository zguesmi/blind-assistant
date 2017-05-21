#!/usr/bin/python3

import time
import RPi.GPIO as GPIO

def getDistance(GPIO_TRIGGER, GPIO_ECHO):
    #Send 10us pulse to trigger
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    start = time.time()
    while GPIO.input(GPIO_ECHO) == 0:
        start = time.time()
    while GPIO.input(GPIO_ECHO) == 1:
        stop = time.time()
    #Calculate pulse length
    duration = stop-start
    #Distance pulse travelled in that time is time
    #multiplied by the speed of sound (cm/s)
    distance = duration * 34000
    #That was the distance there and back so halve the value
    distance = distance / 2
    return distance

def warning(distance, language):
    distance = str(distance)
    pygame.mixer.init()
    pygame.mixer.music.set_volume(1.0)
    pygame.mixer.music.load("sounds/warning" + str(distance) + str(language) + ".mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() is True:
        continue
    pygame.quit()

language = "EN"

#Use BCM GPIO references instead of physical pin numbers
GPIO.setmode(GPIO.BCM)

#Define GPIO to use on Pi
GPIO_TRIGGER = 23
GPIO_ECHO = 24

#Set pins as output and input
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)  # Trigger
GPIO.setup(GPIO_ECHO, GPIO.IN)      # Echo

#Set trigger to False (Low)
GPIO.output(GPIO_TRIGGER, False)

#Allow module to settle
time.sleep(0.1)

while True:
    distance = getDistance(GPIO_TRIGGER, GPIO_ECHO)
    print("Distance : %.1f" % distance)
    try:
        if distance < 100:
            print("you should stop")
            warning(100, language)
        elif distance < 200:
            print("The obstacle is 2 meters ahead")
            warning(200, language)
        elif distance < 400:
            print("There is an obstacle after 4 meters")
            warning(400, language)
    except:
        print("error playing sound")
    time.sleep(0.1)
