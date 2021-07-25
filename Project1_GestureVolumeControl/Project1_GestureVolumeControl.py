import cv2
import time
from mediapipe_HandDetectionModule import HandDetection
import math
from subprocess import call

#########################################
wCam, hCam = 640, 480
pTime = 0
########################################

hand_detector = HandDetection(max_num_hands=1, min_detection_confidence=0.7)
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
volume = 0
texts = '0'

while True:
    ret, frame = cap.read()
    frame = hand_detector.detectHand(frame)  # Detect Hand
    lm = hand_detector.handLandmark(frame, False)  # Detect all landmark of hand

    if len(lm) != 0:

        x1, y1 = lm[4][1], lm[4][2]  # Thump tip landmark co-ordinate
        x2, y2 = lm[8][1], lm[8][2]  # Inder finger tip landmarks co-ordinate
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2  # find center of line connecting point (x1,y1) and (x2,y2)

        length = math.hypot(x2 - x1, y2 - y1)  # find shortest distance between point (x1,y1) and (x2,y2)

        cv2.circle(frame, (x1, y1), 5, (255, 0, 255), -1)
        cv2.circle(frame, (x2, y2), 5, (255, 0, 255), -1)
        cv2.line(frame, (x1, y1), (x2, y2), (255, 30, 235), 2)
        cv2.circle(frame, (cx, cy), 8, (255, 0, 255), -1)

        # Code for controlling Volume Key
        if length < 50:

            cv2.circle(frame, (cx, cy), 8, (0, 255, 0), -1)
            call(["amixer", "-D", "pulse", "sset", "Master", str(0) + "%"])
            volume = 0
            texts = '0'

        elif length > 180:

            cv2.circle(frame, (cx, cy), 8, (0, 0, 255), -1)
            call(["amixer", "-D", "pulse", "sset", "Master", str(100) + "%"])
            volume = 100
            texts = '100'

        else:

            volume = int(((length - 25) / 180) * 100)
            call(["amixer", "-D", "pulse", "sset", "Master", str(volume) + "%"])
            texts = str(volume)

    cv2.rectangle(frame, (50, 150), (85, 400), (0, 255, 0), 2)
    cv2.rectangle(frame, (50, 400 - int(volume * 2.5)), (85, 400), (0, 255, 0), -1)
    cv2.putText(frame, f'{texts}%', (40, 430), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

    # Calculate FPS
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(frame, f"FPS:{int(fps)}", (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    cv2.imshow('Final', frame)

    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
