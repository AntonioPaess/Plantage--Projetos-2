from django.urls import path
from plant.views import *

urlpatterns = [
    path('', HomeView,  name="home"), 
    path('planta/', AddPlanta.as_view(), name="add"),  
    path('area/', AddEspaco.as_view(), name="add-espaco"),
    path('canteiro/<int:espaco_id>/', AddCanteiro.as_view(), name="add-canteiro"), 
    path('plantalist/', ListAllView.as_view(), name="list-all"),
    path('plant/<int:id>', PlantaDetail.as_view(), name="planta-detail"),
    path('teste/', testeview, name="teste"),
]


