import cv2
import os
import numpy as np

# importing custom modules
import sys
sys.path.append('..')
from training.train import ConvNet
from training import hands

cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_PLAIN
model = ConvNet()
model.load()
count = 0

def getHand(idx):
    for key, val in hands.items():
        if idx == val:
            return key

while True:
    count += 1

    ret, frame = cap.read()

    if not ret:
        print("capture failed")
        break

    cv2.rectangle(frame, (100,100), (500, 500), (86, 8, 150), 3)

    cv2.putText(frame, "Place hand in the square",
        (5, 50), font, 2, (86, 8, 150), 2, cv2.LINE_AA)

    cv2.imshow("Play", frame)

    key = cv2.waitKey(1)
    if key % 256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif key % 256 == 32:
        # SPACE pressed
        # store sample image
        img = frame[100:500, 100:500]
        cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (227, 227))
        hand = model.predict(img)
        print("you chose ", hand)

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()


