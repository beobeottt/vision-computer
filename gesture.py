# gesture.py
import cv2
from hand import handDetector

detector = handDetector(detectionCon=0.55)

def count_fingers(image):
    """
    image: numpy array BGR
    return: int số ngón tay giơ lên (0–5)
    """
    img = detector.findHands(image)
    lmList = detector.findPosition(img, draw=False)
    if not lmList:
        return 0
    # xác định trạng thái ngón
    fingerTips = [4,8,12,16,20]
    fingers = []
    # ngón cái
    fingers.append(1 if lmList[fingerTips[0]][1] < lmList[fingerTips[0]-1][1] else 0)
    # 4 ngón
    for i in range(1,5):
        fingers.append(1 if lmList[fingerTips[i]][2] < lmList[fingerTips[i]-2][2] else 0)
    return sum(fingers)
