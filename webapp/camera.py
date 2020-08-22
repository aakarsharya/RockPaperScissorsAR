import cv2

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()
    
    def getFrame(self):
        success, image = self.video.read()
        cv2.rectangle(image, (100,100), (500, 500), (86, 8, 150), 3)
        cv2.putText(image, "Place hand in the square",
            (5, 50), cv2.FONT_HERSHEY_PLAIN, 2, (86, 8, 150), 2, cv2.LINE_AA)
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

def generate(camera):
    while True:
        frame = camera.getFrame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')