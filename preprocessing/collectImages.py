import os
import sys
import cv2

cap = cv2.VideoCapture(0)
n_samples = sys.argv[1]
hands = {'rock': 0, 'paper': 1, 'scissors': 2, 'other': 3}
font = cv2.FONT_HERSHEY_PLAIN

for hand in hands.keys():
    count = 1
    print("Generating", hand, "images")
    while count <= int(n_samples):
        if count == 1:
            cv2.waitKey(5000)

        # Capture frame-by-frame
        ret, frame = cap.read()

        # Draw rectangle where hand should be placed
        cv2.rectangle(frame, (100,100), (500, 500), (86, 8, 150), 3)

        cv2.putText(frame, "Generating {0} image #{1}".format(hand, count),
            (5, 50), font, 2, (86, 8, 150), 2, cv2.LINE_AA)

        cv2.imshow("Generating Training Images", frame)

        # store sample image
        filename = os.path.join(hand, "{0}{1}.jpg".format(hand, count))
        img = frame[100:500, 100:500]
        cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        cv2.imwrite(filename=filename, img=img)
        
        # pause for next image
        cv2.waitKey(30)
        count += 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# # When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
