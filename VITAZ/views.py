from django.shortcuts import render
from django.http.response import StreamingHttpResponse
from .camera import WebCam
import os

# On loading server
camera = WebCam()
# True while signing up
onSignUp = False


def home(request, *args, **kwargs):
    id = camera.getLastID()
    args = {
        "id": id
    }
    return render(request, 'home.html', args)

def getCameraFrame(request, *args, **kwargs):
    return StreamingHttpResponse(
        camera.getCameraFrame(), 
        content_type='multipart/x-mixed-replace; boundary=frame'
    )

def signIn(request, *args, **kwargs):
    id = camera.getLastID()
    args = {
        "id": id
    }

    return render(request, 'home.html', args)
    
def signUp(request, *args, **kwargs):
    onSignUp = True
    args = {
        "onSignUp": onSignUp
    }
    return render(request, 'home.html', args)

def signUpInner(request, *args, **kwargs):
    camera.takeSomeShots()
    return render(request, 'home.html')

def train(request, *args, **kwargs):
    camera.VITAZFaces.train()
    return render(request, 'home.html')

