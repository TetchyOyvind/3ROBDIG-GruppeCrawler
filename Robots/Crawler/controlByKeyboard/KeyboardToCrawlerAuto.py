#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 09:46:00 2024

@author: raspberry
"""

import pygame
import simMotion as robot
import time
import ultrasound

simulation = True

direction = 0
initialDepth = 0
level = 0
armed = False
autoMode = False
rightUp = False
TOLERANCE = 5   #The acceptable offset from setpoint.
                #This vlue will be effectively doubled

#Setup of MPU-board
#i2c = board.I2C()  # uses board.SCL and board.SDA
#mpu = adafruit_mpu6050.MPU6050(i2c)

ultrasound.setup()

print("Press the SPACE-key to engage")
print("Once engaged, use arrow keysto move, or A-key to activate Automatic mode")

#Pygame variables
pygame.init()
screen = pygame.display.set_mode((480, 480))
clock = pygame.time.Clock()
gameRunning = True
dt = 0

robotPos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
robotColor = "red"

def convertRange(oldValue, oldMin, oldMax, newMin, newMax):
    oldRange = oldMax - oldMin
    newRange = newMax - newMin
    newValue = (((oldValue - oldMin) * newRange) / oldRange) + newMin
    return newValue

while gameRunning == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameRunning = False
            
        #Detection of keyboard input
        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:
                armed = not armed
                print("Armert: ", armed)
                if not armed:
                    robot.stop()
                    autoMode= False
            if armed == True:
                if event.key == pygame.K_a:
                    if autoMode == False:
                        autoMode = True
                        print("Auto mode ENGAGED!")
                    elif autoMode == True:
                        autoMode = False
                        print("Auto mode DISENGAGED!")
            if armed == True and autoMode == False:
                if event.key == pygame.K_UP:
                    print("Up arrow pressed")
                    direction = 1
                elif event.key == pygame.K_DOWN:
                    print("Down arrow pressed")
                    direction = -1
                elif event.key == pygame.K_LEFT and direction != 1:
                    print("Left arrow pressed")
                    direction = 2
                elif event.key == pygame.K_RIGHT and direction != 1:
                    print("Right arrow pressed")
                    direction = 3
                if direction == 1:
                    if event.key == pygame.K_LEFT:
                        robot.autoSteer(50)
                        direction = 21
                    elif event.key ==pygame.K_RIGHT:
                        robot.autoSteer(-50)
                        direction = 31
                    if event.type == pygame.KEYUP:
                        if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                            direction = 1
                            robot.autoSteer(0)
                            print("Direction released!")
                robot.direction(direction)
        elif event.type == pygame.KEYUP:
            if armed == True and autoMode == False:
                if event.key in [pygame.K_UP, pygame.K_DOWN]:
                    print("Key released")
                    direction = 0
                    
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    if direction == 21 or direction == 31:
                        direction = 1
                        robot.autoSteer(0)
                        print("Direction released!")
                    if direction == 2 or direction == 3:
                        direction = 0
                robot.direction(direction)
    if autoMode and armed:
        if level == 0:
            print("Initial level. Using depth sesor.")
            initialDepth = ultrasound.getDistance() #Change to current read value from depth sensor before start.
            print("Initial depth is ", initialDepth)
            
            #Check accelerometer to set rightUp to correct value
#            acceleration = mpu.acceleration
#            accY = acceleration[1]
#            if (accY > 0.5):
#                rightUp = True
#                print(accY)
#                print("Right is up!")
#            elif(accY < 0):
#                rightUp = False
#                print("Right is down!")
            
            level = 1
            print("Starting level ", level, " using vision")   

            #Auto-program 
        if level == 1:
            if simulation == True:
                i = 0
                while i < 15:
                    print(i, " meter")
                    print("...")
                    time.sleep(2)
                    i += 1
                
                print("Turn 90 deg")
                time.sleep(1)
                print("Forward 1 level")
                time.sleep(1)
                print("Turn 90 deg")
                time.sleep(1)
                level = 1         

            if simulation == False:

                print("Level 1, using depth sensor for initial level")
                
                depth = ultrasound.getDistance()
                print("Depth: ", depth)
                time.sleep(0.5)
                
                difference = depth - initialDepth
                print("Difference: ", difference)
                
                adjustment = difference
                
                if adjustment > 75:
                    adjustment = 75
                
                if difference <= -TOLERANCE:
                    print("Høyre")
                    robot.autoSteer(adjustment)
                    direction = 31
                    
                elif difference >= TOLERANCE:
                    print("Venstre")
                    robot.autoSteer(adjustment)
                    direction = 21
                    
                elif difference < TOLERANCE and difference > -TOLERANCE:
                    direction = 1
                    
                else:
                    direction = 0
                
                #Emergency stop
                if depth < 15:
                    autoMode = False
                    armed = False
                    direction = 0
                    
                endDetected = False
                
                if endDetected:
                    level = level + 1
                    direction = 0
                    
                robot.direction(direction)
            #stepDownTurn()
            #Turn 90 deg downwards, drive one level down,
            #turn another 90 deg            

    
    #Pygame
    screen.fill("purple")
    
    if armed:
        robotColor = "green"
        
        if autoMode:
            robotColor = "blue"
    elif armed == False:
            robotColor = "red"
    
    #if direction == 1:
     #   robotPos.y -= 100 * dt
      #  #print(direction)
    #elif direction == -1:
     #   robotPos.y += 100 * dt
    
    pygame.draw.circle(screen, robotColor, robotPos, 20)
    
    
    
    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
ultrasound.stop()

