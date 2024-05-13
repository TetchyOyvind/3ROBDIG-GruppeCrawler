import cv2
import numpy as np

# Last inn video
cap = cv2.VideoCapture(r'C:\Users\Andre\Downloads\Skrogvasktest.mp4')


while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Konverter til HSV-fargerom
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Definer rekkevidden for grønn (alger) og brun (skjell)
    lower_green = np.array([25, 100, 50])
    upper_green = np.array([55, 255, 255])
    lower_brown = np.array([10, 100, 20])  # Juster disse verdiene
    upper_brown = np.array([20, 255, 200])  # Juster disse verdiene

    # Lag masker
    green_mask = cv2.inRange(hsv, lower_green, upper_green)
    brown_mask = cv2.inRange(hsv, lower_brown, upper_brown)
    combined_mask = cv2.bitwise_or(green_mask, brown_mask)

    # Vis resultatene
    cv2.imshow('Original', frame)
    cv2.imshow('Green Algae Detection', green_mask)
    cv2.imshow('Shell Growth Detection', brown_mask)
    cv2.imshow('Combined Detection', combined_mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
