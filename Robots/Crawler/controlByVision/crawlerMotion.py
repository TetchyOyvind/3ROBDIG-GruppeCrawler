#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 10:55:35 2024

@author: raspberry
"""

import RPi.GPIO as GPIO          
from time import sleep
import pigpio

# Initialize the pigpio library
pi = pigpio.pi()


# Define the GPIO pin connected to the VESC
ESC1_GPIO = 12
ESC2_GPIO = 13

# Define the pulse width values for the ESC
PULSE_WIDTH_MIN = 1000  # Minimum pulse width in microseconds
PULSE_WIDTH_MAX = 2000  # Maximum pulse width in microseconds

idle = 1500
marsjFart = 1700
marsjRevers = 1300

trim = 14

forwardLeft = 200
forwardRight = - forwardLeft + trim

backwardRight = 200
backwardLeft = - backwardRight + trim

def initialize():
    pi.set_servo_pulsewidth(ESC1_GPIO, 0)
    pi.set_servo_pulsewidth(ESC2_GPIO, 0)

def set_speed(speedLeft, speedRight):
    #if speedLeft > marsjFart:
    #    speedLeft = marsjFart
    #elif speedLeft < marsjRevers:
    #    speedLeft = marsjRevers
    #if speedRight > marsjFart:
    #    speedRight = marsjFart
    #elif speedRight < marsjRevers:
    #    speedRight = marsjRevers
        
    pi.set_servo_pulsewidth(ESC1_GPIO, idle + speedLeft)
    pi.set_servo_pulsewidth(ESC2_GPIO, idle + speedRight)
    
    print("Left: ", speedLeft, "Right: ", speedRight)


# Define functions for movement
def forwardBil():
    set_speed(forwardLeft, forwardRight)


def backwardBil():
    set_speed(backwardLeft, backwardRight)

def venstreBil():
    set_speed(backwardLeft, forwardRight)
    
def autoLeft(power):
    #power = powerL
    print(power)
    set_speed(forwardLeft, -forwardRight - power)


def hoyreBil():
    set_speed(forwardLeft, backwardRight)

def autoRight(power):
    print(power)
    set_speed(forwardLeft + power, -forwardRight)
    
def autoSteer(power):
    set_speed(forwardLeft - power, forwardRight - power)

def stopBil():
    pi.set_servo_pulsewidth(ESC1_GPIO, idle)
    pi.set_servo_pulsewidth(ESC2_GPIO, idle)
    
def cleanup():
    GPIO.cleanup()

def goForward():
    print("Gï¿½r fremover!")
    forwardBil()

def goBackward():
    print("Gï¿½r bakover!")
    backwardBil()

def goLeft():
    print("Snur venstre!")
    venstreBil()

def goRight():
    print("Snur hï¿½yre!")
    hoyreBil()
    
def stop():
    print("Stoppet!")
    stopBil()
    
def goDirection(directionValue):
    if direction == 0:
        stop()
    elif direction == 1:
        goForward()
    elif direction == -1:
        goBackward()
    elif direction == 2:
        goLeft()
    elif direction == 3:
        goRight()
#    elif direction == 21:
#        autoLeft(100)
#    elif direction == 31:
#        autoRight(100)
