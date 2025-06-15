# dnt.py
import cv2
import os
from hand import handDetector

# Load finger images exactly like original script
FolderPath = "Fingers"
lst = sorted(os.listdir(FolderPath))
lst_imgs = []
for fname in lst:
    img = cv2.imread(os.path.join(FolderPath, fname))
    lst_imgs.append(img)

# Initialize hand detector
detector = handDetector(detectionCon=0.55)
finger_ids = [4, 8, 12, 16, 20]

def detect_and_overlay(frame):
    """
    Detect hand, count raised fingers, overlay corresponding image and return count
    """
    img = detector.findHands(frame)
    lmList = detector.findPosition(img, draw=False)
    count = 0
    if lmList:
        fingers = []
        # Thumb logic: compare x of tip and its landmark
        if lmList[finger_ids[0]][1] < lmList[finger_ids[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        # Other fingers: compare y of tip and its lower landmark
        for i in range(1, 5):
            if lmList[finger_ids[i]][2] < lmList[finger_ids[i] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        count = sum(fingers)
        # Overlay corresponding image from lst_imgs
        overlay = lst_imgs[count]
        h, w, _ = overlay.shape
        frame[0:h, 0:w] = overlay
        # Draw count box and text
        cv2.rectangle(frame, (0, 200), (150, 400), (0, 255, 0), -1)
        cv2.putText(frame, str(count), (30, 390), cv2.FONT_HERSHEY_PLAIN, 10, (255, 0, 0), 5)
    return frame, count
