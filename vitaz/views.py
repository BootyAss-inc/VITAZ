from django.shortcuts import redirect, render
from django.http.response import StreamingHttpResponse
from django.forms import Form, TextInput

from .utility.camera import Camera
from .utility.camerahandler import CameraHandler
from .utility import logger


cameraHandler = CameraHandler()


class VitazForm(Form):
    fields = ['name']
    widgets = {
        'name': TextInput(attrs={
            'class': 'popup-inp',
            'placeholder': 'Name'
        })
    }


def defaultArgs():
    args = {
        'error': False,
        'multipleFaces': False,
        'noFaceDetected': False,
        'showAcces': False,
        'accessGranted': False,
        'doublePass': False,
        'doubleDirection': False,
        'direction': False,
        'pressedSignUp': False,
        'userName': None
    }
    return args


def home(request, *args, **kwargs):
    args = defaultArgs()
    return render(request, 'home.html', args)


def inCameraFrame(request, *args, **kwargs):
    return StreamingHttpResponse(
        cameraHandler.getInCameraFrame(),
        content_type='multipart/x-mixed-replace; boundary=frame'
    )


def outCameraFrame(request, *args, **kwargs):
    return StreamingHttpResponse(
        cameraHandler.getOutCameraFrame(),
        content_type='multipart/x-mixed-replace; boundary=frame'
    )


def signIn(request, *args, **kwargs):
    args = defaultArgs()
    args.update(cameraHandler.inCameraRecognizeFace())
    return render(request, 'home.html', args)


def signOut(request, *args, **kwargs):
    args = defaultArgs()
    args.update(cameraHandler.outCameraRecognizeFace())
    return render(request, 'home.html', args)


def signUp(request, *args, **kwargs):
    args = defaultArgs()
    args['pressedSignUp'] = True

    if request.method == 'POST':
        data = request.POST
        form = VitazForm(data)
        if form.is_valid():
            name = data['popup']
            if name:
                args.update(cameraHandler.inCameraSaveFace(name))
                if not args['error']:
                    return redirect('home')

    form = VitazForm()
    args['form'] = form
    return render(request, 'home.html', args)


def log(request, *args, **kwargs):
    with open('log.log', 'r') as fileHandle:
        data = fileHandle.readlines()
    args = {
        'data': data
    }
    return render(request, 'log.html', args)
