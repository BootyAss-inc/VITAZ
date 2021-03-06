from django.urls import path
from . import views


# URL router config for VITAZ
urlpatterns = [
    # home page
    path('', views.home, name='home'),
    # insert camera frame into page
    path('inCameraFrame', views.inCameraFrame, name='inCameraFrame'),
    path('outCameraFrame', views.outCameraFrame, name='outCameraFrame'),
    # on signIn button click
    path('signIn', views.signIn, name='signIn'),
    # on signOut button click
    path('signOut', views.signOut, name='signOut'),
    # on signUp button click
    path('signUp', views.signUp, name='signUp'),
    # display log file
    path('log', views.log, name='log'),
    ]
