from django.urls import path, include
from .views import (logout,
                    SignUpView,
                    LoginView,
                    ChangePasswordView,
                    DeactivateProfileView,
                    ActivateProfileView)

from django.contrib.auth.views import (PasswordResetView,
                                       PasswordResetConfirmView,
                                       PasswordResetCompleteView,
                                       PasswordResetDoneView)

urlpatterns = [
    path('logout/', logout, name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('changepassword/', ChangePasswordView.as_view(), name='change_password'),
    path('deactivate/', DeactivateProfileView.as_view(), name='deactivate_profile'),
    path('activate/', ActivateProfileView.as_view(), name='activate_profile'),

    path('password_reset/', PasswordResetView.as_view(template_name='reset_password.html'), name='reset_password'),
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),

]
