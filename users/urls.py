from django.urls import path
from .views import logout, SignUpView, LoginView, ChangePasswordView, RecoverView
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView, PasswordResetDoneView

urlpatterns = [
    path('logout/', logout, name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('changepassword/', ChangePasswordView.as_view(), name='change_password'),
    path('recoverpassword/', RecoverView.as_view(), name='recover_password'),

    path('password_reset/', PasswordResetView, {'template_name': 'auth/password_reset.html', 'email_template_name': 'auth/password_reset_email.html', 'from_email': 'filipevilanovaneiva@gmail.com'}, name='password-reset'),
    
]
