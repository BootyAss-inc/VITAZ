from django.shortcuts import render
from django.http.response import StreamingHttpResponse
from .camera import WebCam


camera = WebCam()


def home(request, *args, **kwargs):
    return render(request, 'home.html')

def getCameraFrame(request, *args, **kwargs):
    return StreamingHttpResponse(
        camera.getCameraFrame(), 
        content_type='multipart/x-mixed-replace; boundary=frame'
    )

def signIn(request, *args, **kwargs):
    return render(request, 'home.html')
    
def signUp(request, *args, **kwargs):
    return render(request, 'home.html')

