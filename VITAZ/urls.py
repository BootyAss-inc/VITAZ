from django.urls import path
from . import views

# URL router config for VITAZ 
urlpatterns = [
    path('', views.home, name='home'),
    path('camera', views.getCameraFrame, name='camera'),
    path('signIn', views.signIn, name='signIn'),
    path('signUp', views.signUp, name='signUp')
]