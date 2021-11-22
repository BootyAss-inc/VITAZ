from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request, *args, **kwargs):
    return HttpResponse('home page')

def hello(request, *args, **kwargs):
    return HttpResponse('hello')
