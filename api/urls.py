from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import UserPostsList, UserPostDetail, UserInvitationsList, UserInvitationDetail

urlpatterns = [
    path('token-auth/', obtain_auth_token),
    path('my-posts/', UserPostsList.as_view(), name=UserPostsList.name),
    path('my-posts/<int:pk>', UserPostDetail.as_view(), name=UserPostDetail.name),
    path('my-invitations/', UserInvitationsList.as_view(), name=UserInvitationsList.name),
    path('my-invitations/<int:pk>', UserInvitationDetail.as_view(), name=UserInvitationDetail.name),
]