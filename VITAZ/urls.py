from django.urls import path
from . import views

# URL router config for VITAZ 
urlpatterns = [
    path('', views.home, name='home'),
    path('webcam', views.webcam_get_frame, name='webcam')
]