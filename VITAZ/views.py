from django.shortcuts import render
from django.http import HttpResponse

# from django.views.decorators import gzip

# from threading import Thread
from django.http.response import StreamingHttpResponse
import cv2


def home(request, *args, **kwargs):
    return render(request, 'home.html')



class WebCam(object):
    def __init__(self):
        self.webcam = cv2.VideoCapture(0)

    def __del__(self):
        self.webcam.release()

    def get_frame(self):
        ret, frame = self.webcam.read()
        ret, jpeg = cv2.imencode('.jpeg', frame)
        return jpeg.tobytes()

def gen_frame_img(webcam):
    while True:
        frame = webcam.get_frame()
        yield ( b'--frame\r\n'
                b'content-type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def webcam_get_frame(request):
    return StreamingHttpResponse(
        gen_frame_img(WebCam()), 
        content_type='multipart/x-mixed-replace; boundary=frame'
    )