from django.shortcuts import redirect, render
from django.http.response import StreamingHttpResponse
from django.forms import Form, TextInput

from .camera import Camera


camera = Camera()


class VitazForm(Form):
    fields = ['name']
    widgets = {
        'name': TextInput(attrs={
            'class': 'popup-inp',
            'placeholder': 'Name'
        })
    }


def home(request, *args, **kwargs):
    args= { 
        'ret': False,
        'showAccess': False,
        'access': False,
        'pop': False
    }
    return render(request, 'home.html', args)

def cameraFrame(request, *args, **kwargs):
    return StreamingHttpResponse(
        camera.getCameraFrame(), 
        content_type='multipart/x-mixed-replace; boundary=frame'
    )

def signIn(request, *args, **kwargs):
    ret, access, name = camera.recognizeFace()
    args= { 
        'ret': ret,
        'showAccess': not ret,
        'access': access,
        'pop': False,
        'NAME': name
    }
    return render(request, 'home.html', args)
    

def signUp(request, *args, **kwargs):
    ret = False
    if request.method == 'POST':
        data = request.POST
        form = VitazForm(data)
        if form.is_valid():
            name = data['popup']
            if name:
                ret = camera.saveFace(name)
                if not ret:
                    return redirect('home')


    form = VitazForm()
    args= { 
        'ret': ret,
        'showAccess': False,
        'access': False,
        'pop': True,
        'form': form
    }
    return render(request, 'home.html', args)


