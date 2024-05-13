import cv2
import numpy as np

# Opprett et VideoCapture-objekt
cap = cv2.VideoCapture('C:/Users/Andre/Downloads/VideoGroe5.mp4')

# Definer HSV-grenser for fargen grønn
lower_green = np.array([40, 40, 40])
upper_green = np.array([70, 255, 255])

# Opprett en CLAHE-objekt for kontrastforbedring
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))

# Tester om videoen ble åpnet riktig
if not cap.isOpened():
    print("Kan ikke åpne videoen.")
else:
    # Loop gjennom videoen frame for frame
    while True:
        ret, frame = cap.read()  # Les neste frame

        if not ret:
            print("Kan ikke motta frame (kanskje stream slutt?). Avslutter ...")
            break

        # Konverter bildet til LAB-fargerom for å anvender CLAHE på L-kanalen
        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        l2 = clahe.apply(l)
        lab = cv2.merge((l2, a, b))
        frame_contrast_enhanced = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

        # Utfører fargeterskeling for å identifisere grønne områder
        hsv = cv2.cvtColor(frame_contrast_enhanced, cv2.COLOR_BGR2HSV)
        mask_green = cv2.inRange(hsv, lower_green, upper_green)

        # Finner konturer i de grønne områdene og tegner dem
        contours, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(frame_contrast_enhanced, contours, -1, (0, 255, 0), 2)  # Tegn med grønn farge

        # Utfører Canny-kantdeteksjon
        edges = cv2.Canny(cv2.cvtColor(frame_contrast_enhanced, cv2.COLOR_BGR2GRAY), 50, 150)

        # Bruk Hough Line Transform for å detektere linjesegmenter
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=50, minLineLength=100, maxLineGap=10)
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(frame_contrast_enhanced, (x1, y1), (x2, y2), (255, 0, 0), 3)  # Tegner linjene med blått

        # Viser det kombinerte bildet med detekterte groeområder og linjer
        cv2.imshow('Detected Green Areas and Lines', frame_contrast_enhanced)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Slipp VideoCapture-objektet og lukk alle OpenCV-vinduer
cap.release()
cv2.destroyAllWindows()
