from django.urls import path
from .views import index, logout, SignUpView, LoginView, ChangePasswordView

urlpatterns = [
    path('logout/', logout, name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('changepassword/', ChangePasswordView.as_view(), name='change_password'),
]