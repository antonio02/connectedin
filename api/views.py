from rest_framework import generics, permissions
from posts.models import Post, Profile
from profiles.models import Profile, Invitation
from .serializers import UserPostSerializer, UserInvitationSerializer


# Create your views here.

class UserPostsList(generics.ListCreateAPIView):
    serializer_class = UserPostSerializer
    name = 'user-posts-list'
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(profile__user=user)

    def perform_create(self, serializer):
        serializer.save(profile=Profile.objects.get(user=self.request.user))


class UserPostDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserPostSerializer
    name = 'user-post-detail'
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(profile__user=user)


class UserInvitationsList(generics.ListAPIView):
    serializer_class = UserInvitationSerializer
    name = 'user-invitation-list'
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def get_queryset(self):
        user = self.request.user
        return Invitation.objects.filter(sender__user=user)


class UserInvitationDetail(generics.RetrieveDestroyAPIView):
    serializer_class = UserInvitationSerializer
    name = 'user-invitation-detail'
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def get_queryset(self):
        user = self.request.user
        return Invitation.objects.filter(sender__user=user)
