
from django.contrib import admin
from django.urls import path, include
from plant.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView, name="home"),
    path('',include('a_users.urls'))
]