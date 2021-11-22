from django.urls import path
from . import views

# URL router config for VITAZ 
urlpatterns = [
    path('hello/', views.hello),
    path('', views.home)
]