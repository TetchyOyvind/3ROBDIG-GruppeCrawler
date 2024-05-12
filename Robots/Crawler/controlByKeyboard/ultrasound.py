#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 10:33:56 2024

@author: raspberry
"""

import RPi.GPIO as GPIO
import time

# Define GPIO pins
TRIG = 22
ECHO = 27

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    GPIO.output(TRIG, False)
    time.sleep(2)  # Allow module to settle

def getDistance():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)  # Pulse for 10us
    GPIO.output(TRIG, False)
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150  # Speed of sound at sea level is 343 m/s
    distance = round(distance, 2)
    return distance

def main():
    setup()
    while True:
        distance = getDistance()
        print("Distance: {} cm".format(distance))
        time.sleep(1)  # Wait for 1 second before next reading

def stop():
    GPIO.cleanup()