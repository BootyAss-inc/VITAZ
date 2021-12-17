from django.shortcuts import redirect, render
from django.http.response import StreamingHttpResponse
from django.forms import Form, TextInput

from .camera import Camera
from . import logger


inCamera = Camera(0)
outCamera = Camera(1)


logger.saveInfo('server started')


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
        inCamera.getCameraFrame(),
        content_type='multipart/x-mixed-replace; boundary=frame'
    )

def outCameraFrame(request, *args, **kwargs):
    return StreamingHttpResponse(
        outCamera.getCameraFrame(),
        content_type='multipart/x-mixed-replace; boundary=frame'
    )


def signIn(request, *args, **kwargs):
    args = defaultArgs()
    args.update(inCamera.recognizeFace())
    return render(request, 'home.html', args)

def signOut(request, *args, **kwargs):
    args = defaultArgs()
    args.update(outCamera.recognizeFace())
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
                args.update(inCamera.saveFace(name))
                if not args['error']:
                    return redirect('home')

    form = VitazForm()
    args['form'] = form
    return render(request, 'home.html', args)
