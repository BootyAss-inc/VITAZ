from django.shortcuts import render
from django.http import HttpResponse

from django.http.response import StreamingHttpResponse
from django.views.decorators import gzip

from threading import Thread
import cv2

# Create your views here.
@gzip.gzip_page
def home(request, *args, **kwargs):
    try:
        cam = VideoCam()
        return StreamingHttpResponse(
            gen(cam),
            content_type='multipart/x-mixed-replace;boundary=frame'
        )
    except:
        pass
    return render(request, 'home.html')

class VideoCam(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.grabbed, self.frame = self.video.read()
        Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        _, img = cv2.imencode('.jpg', self.frame)
        return img.tobytes()

    def update(self):
        while True:
            self.grabbed, self.frame = self.video.read()
    
def gen(camera):
    while True:
        frame = camera.get_frame()
        yield  (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n'
        )