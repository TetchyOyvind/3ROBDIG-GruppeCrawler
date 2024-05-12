#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 17:38:35 2024

@author: raspberry
"""

import cv2
import numpy as np
import bilMotion as robot

# Definer funksjonene for robotens bevegelser
def forward():
    robot.forwardBil()  # Implementer funksjonen for ï¿½ bevege roboten fremover

def backward():
    robot.backwardBil()  # Implementer funksjonen for ï¿½ bevege roboten bakover

def rotate_left():
    robot.venstreBil()  # Implementer funksjonen for ï¿½ rotere roboten til venstre

def rotate_right():
    robot.hoyreBil()  # Implementer funksjonen for ï¿½ rotere roboten til hï¿½yre

def stop():
    robot.stop()  # Implementer funksjonen for ï¿½ stoppe roboten

# Start videostrï¿½mmen
cap = cv2.VideoCapture(0)

while True:
    # Les inn bildet fra videostrï¿½mmen
    _, frame = cap.read()

    # Konverter bildet til HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Definer omrï¿½det for rï¿½d farge i HSV
    lower_red = np.array([0, 120, 70])
    upper_red = np.array([10, 255, 255])

    # Lag en maske med den rï¿½de fargen
    mask = cv2.inRange(hsv, lower_red, upper_red)

    # Utfï¿½r kantdeteksjon
    edges = cv2.Canny(mask, 75, 150)

    # Utfï¿½r Hough Line Transform
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 50, maxLineGap=50)

    if lines is not None:
        # Initialiser summen av start- og sluttpunkter
        x1_sum = 0
        y1_sum = 0
        x2_sum = 0
        y2_sum = 0

        # Summer start- og sluttpunktene for alle linjene
        for line in lines:
            x1, y1, x2, y2 = line[0]
            x1_sum += x1
            y1_sum += y1
            x2_sum += x2
            y2_sum += y2

        # Beregn gjennomsnittet av start- og sluttpunktene for ï¿½ fï¿½ den representative linjen
        x1_avg = x1_sum // len(lines)
        y1_avg = y1_sum // len(lines)
        x2_avg = x2_sum // len(lines)
        y2_avg = y2_sum // len(lines)

        # Tegn den representative linjen
        cv2.line(frame, (x1_avg, y1_avg), (x2_avg, y2_avg), (0, 255, 0), 5)

        # Beregn vinkelen til linjen
        angle = np.arctan2(y2_avg - y1_avg, x2_avg - x1_avg) * 180. / np.pi

        # Gi instruksjoner basert pï¿½ vinkelen til linjen
        if angle < -75:
            rotate_right()  # Roter til hï¿½yre
        elif angle > 75:
            rotate_left()  # Roter til venstre
        else:
            forward()  # Beveg fremover
    else:
        stop()  # Stopp
    print(angle)

    # Vis bildet
    cv2.imshow("Frame", frame)

    # Avslutt lï¿½kken hvis 'q' blir trykket
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Frigi ressursene
cap.release()
cv2.destroyAllWindows()
