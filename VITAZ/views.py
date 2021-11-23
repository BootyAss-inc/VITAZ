from django.shortcuts import render
from django.http.response import StreamingHttpResponse
import cv2


def home(request, *args, **kwargs):
    return render(request, 'home.html')



class WebCam(object):
    def __init__(self):
        self.camNum = 0
        self.camera = cv2.VideoCapture(self.camNum)

    def __del__(self):
        self.camera.release()

    def getFrame(self):
        _, frame = self.camera.read()
        _, jpeg = cv2.imencode('.jpeg', frame)
        return jpeg.tobytes()

    def changeCamera(self):
        self.camera.release()
        self.camNum += 1
        self.camera = cv2.VideoCapture(self.camNum)


def getCameraFrameAsImage(camera):
    while True:
        frame = camera.getFrame()
        yield ( b'--frame\r\n'
                b'content-type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def getCameraFrame(request):
    return StreamingHttpResponse(
        getCameraFrameAsImage(WebCam()), 
        content_type='multipart/x-mixed-replace; boundary=frame'
    )