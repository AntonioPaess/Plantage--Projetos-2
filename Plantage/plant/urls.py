from django.urls import path
from plant.views import *

urlpatterns = [
    path('', HomeView, name="home"), 
    path('planta/', AddPlanta.as_view(), name="add"),  
]

