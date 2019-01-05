from django.urls import path
from .views import *

urlpatterns = [
    path('<str:username>', profile, name='profile'),
]