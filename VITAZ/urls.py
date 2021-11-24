from django.urls import path
from . import views


# URL router config for VITAZ 
urlpatterns = [
    # home page
    path('', views.home, name='home'),
    # insert camera frame into page
    path('camera', views.getCameraFrame, name='camera'),
    # on signIn button click
    path('signIn', views.signIn, name='signIn'),
    # on signUp button click
    path('signUp', views.signUp, name='signUp'),
    # on Inner signUp button click
    path('signUpInner', views.signUpInner, name='signUpInner'),
    path('train', views.train, name='train')
]