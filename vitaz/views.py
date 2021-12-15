from django.shortcuts import redirect, render
from django.http.response import StreamingHttpResponse
from django.forms import Form, TextInput

from .camera import Camera
from . import logger

camera = Camera()


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


logger.saveInfo('server started')


def home(request, *args, **kwargs):
    args = defaultArgs()
    return render(request, 'home.html', args)


def cameraFrame(request, *args, **kwargs):
    return StreamingHttpResponse(
        camera.getCameraFrame(),
        content_type='multipart/x-mixed-replace; boundary=frame'
    )


def signIn(request, *args, **kwargs):
    args = defaultArgs()
    args.update(camera.recognizeFace())
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
                args.update(camera.saveFace(name))
                if not args['error']:
                    return redirect('home')

    form = VitazForm()
    args['form'] = form
    return render(request, 'home.html', args)
