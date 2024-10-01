from django.urls import path
from plant.views import *

urlpatterns = [
    path('', HomeView, name="home"),  
]