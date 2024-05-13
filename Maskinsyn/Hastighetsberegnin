# Importing necessary libraries
import cv2
import numpy as np

# Åpner videoen
cap = cv2.VideoCapture('C:/Users/Andre/DownLoads/VideoGroe5.mp4')

# Leser videoen og konverter det til gråskala
ret, frame1 = cap.read()
prev_img = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)

# Oppretter et maskebilde for tegning (flytvektorene)
mask = np.zeros_like(frame1)
mask[..., 1] = 255

while True:
    ret, frame2 = cap.read()
    if not ret:
        break
    next_img = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    # Beregner den optiske flyten ved hjelp av Farneback-metoden
    flow = cv2.calcOpticalFlowFarneback(prev_img, next_img, None, 0.5, 3, 15, 3, 5, 1.2, 0)

    # Beregner størrelsen og vinkelen på 2D-vektorene
    magnitude, angle = cv2.cartToPolar(flow[..., 0], flow[..., 1])

    # Sett bildehue i henhold til den optiske flytretningen
    mask[..., 0] = angle * 180 / np.pi / 2

    # Bildeverdien i henhold til den optiske flytstørrelsen (normalisert)
    mask[..., 2] = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX)

    # Konverter HSV til RGB (for visning)
    rgb = cv2.cvtColor(mask, cv2.COLOR_HSV2BGR)

    # Vis resultatet
    cv2.imshow('frame', rgb)
    k = cv2.waitKey(30) & 0xff
    if k == 27:  # Avslutt ved ESC
        break

    # Oppdater det forrige bildet
    prev_img = next_img

cap.release()
cv2.destroyAllWindows()
