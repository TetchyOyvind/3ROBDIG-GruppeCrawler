import RPi.GPIO as GPIO          
from time import sleep
GPIO.cleanup()
# Define the GPIO pins
in1 = 24
in2 = 23
in3 = 27
in4 = 22
en1 = 12
en2 = 13
temp1=1

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)
GPIO.setup(en1, GPIO.OUT)
GPIO.setup(en2, GPIO.OUT)
GPIO.output(in1, GPIO.LOW)
GPIO.output(in2, GPIO.LOW)
GPIO.output(in3, GPIO.LOW)
GPIO.output(in4, GPIO.LOW)
p1 = GPIO.PWM(en1, 1000)
p2 = GPIO.PWM(en2, 1000)
p1.start(50)
p2.start(50)

# Define functions for movement
def forwardBil():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.HIGH)

def backwardBil():
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.LOW)

def venstreBil():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.LOW)   
    
def hoyreBil():
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.HIGH)

def stopBil():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)

def set_speed(speed):
    p1.ChangeDutyCycle(speed)
    p2.ChangeDutyCycle(speed)

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
    
def direction(direction):
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
