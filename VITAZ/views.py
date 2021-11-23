from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request, *args, **kwargs):
    return render(request, 'homepage.html')

def hello(request, *args, **kwargs):
    return render(request, 'hello.html')

