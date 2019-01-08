from django.urls import path
from .views import *

urlpatterns = [
    path('<str:key>', search, name='search'),
    path('', search, name='search'),
]