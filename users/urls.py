from django.urls import path
from .views import index, logout, SignUpView, LoginView

urlpatterns = [
    path('', index, name='index'),
    path('logout/', logout, name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
]