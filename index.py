#!/usr/bin/python3

import time
import RPi.GPIO as GPIO

# Get distance between the user and the nearest obstacle
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

# Play warnings according to distance and language
def play_sound(distance, language):
    distance = str(distance)
    pygame.mixer.init()
    pygame.mixer.music.set_volume(1.0)
    pygame.mixer.music.load("resources/sounds/" + language + "/warning" + str(distance) + ".mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() is True:
        continue
    pygame.quit()

# play warnings
def warn(distance):
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


# Choose language of warnings
language = "EN"

# Use BCM GPIO references instead of physical pin numbers
GPIO.setmode(GPIO.BCM)

# Define GPIO to use on Pi
GPIO_TRIGGER = 23
GPIO_ECHO = 24

# Set pins as output and input
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)  # Trigger
GPIO.setup(GPIO_ECHO, GPIO.IN)      # Echo

# Set trigger to False (Low)
GPIO.output(GPIO_TRIGGER, False)

# Allow module to settle
time.sleep(0.1)

while True:
    distance = getDistance(GPIO_TRIGGER, GPIO_ECHO)
    print("Distance : %.1f" % distance)
    warn(distance)
    time.sleep(0.1)
