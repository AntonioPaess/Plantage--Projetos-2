from django.urls import path
from . import views

app_name = 'plant'

urlpatterns = [
    path('', views.HomeViews.as_view(). name = 'home')
]