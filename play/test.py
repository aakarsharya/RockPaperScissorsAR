import cv2
import os
import numpy as np
from keras.models import load_model

cap = cv2.VideoCapture(0)
hands = {'rock': 0, 'paper': 1, 'scissors': 2, 'other': 3}
font = cv2.FONT_HERSHEY_PLAIN
model = load_model("rps_model.h5")
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

    # print("You played ", hand)
    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        # store sample image
        img = frame[100:500, 100:500]
        cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (227, 227))
        print(img.shape)
        # prediction
        prediction = model.predict(np.asarray([img]))
        hand = getHand(np.argmax(prediction))
        print("you chose ", hand)

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()


