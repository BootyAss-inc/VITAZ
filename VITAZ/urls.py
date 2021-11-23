from django.urls import path
from . import views

# URL router config for VITAZ 
urlpatterns = [
    path('', views.home),
    path('hello/', views.hello)
]