from django.urls import path
from plant.views import *

urlpatterns = [
    path('', HomeView, name="home"), 
    path('planta/', AddPlanta.as_view(), name="add"),  
    path('area/', AddEspaco.as_view(), name="add-espaco"),
    path('canteiro/', AddCanteiro.as_view(), name="add-canteiro"),
]

