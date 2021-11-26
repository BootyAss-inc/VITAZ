from django.urls import path
from . import views


# URL router config for VITAZ 
urlpatterns = [
    # home page
    path('', views.home, name='home'),
    # insert camera frame into page
    path('cameraFrame', views.cameraFrame, name='cameraFrame'),
    # on signIn button click
    path('signIn', views.signIn, name='signIn'),
    # on signUp button click
    path('signUp', views.signUp, name='signUp'),
]