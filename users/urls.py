from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('<str:username>', profile, name='profile'),
    path('logout/', logout, name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
]