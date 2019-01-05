from django.urls import path
from .views import *

urlpatterns = [
    path('<str:username>/', profile, name='profile'),
    path('<str:username>/invite/', invite_profile, name='invite_profile'),
]