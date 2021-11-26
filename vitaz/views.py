from django.shortcuts import render
from django.http.response import StreamingHttpResponse
from .camera import Camera


camera = Camera()


def home(request, *args, **kwargs):
    args= { 
        'showAccess': False,
        'access': False
    }
    return render(request, 'home.html', args)

def cameraFrame(request, *args, **kwargs):
    return StreamingHttpResponse(
        camera.getCameraFrame(), 
        content_type='multipart/x-mixed-replace; boundary=frame'
    )

def signIn(request, *args, **kwargs):
    ret, access = camera.recognizeFace()
    args= { 
        'ret': ret,
        'showAccess': not ret,
        'access': access
    }
    return render(request, 'home.html', args)
    
def signUp(request, *args, **kwargs):
    ret = camera.saveFace()
    args= { 
        'ret': ret,
        'showAccess': False,
        'access': False
    }
    return render(request, 'home.html', args)


