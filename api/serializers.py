from rest_framework import serializers
from posts.models import Post
from profiles.models import Invitation


class UserPostSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='profile.user.username')

    class Meta:
        model = Post
        fields = ('id', 'image', 'post_text', 'post_date', 'username')

class UserInvitationSerializer(serializers.ModelSerializer):
    sender_username = serializers.ReadOnlyField(source='sender.user.username')
    receiver_username = serializers.ReadOnlyField(source='receiver.user.username')

    class Meta:
        model = Invitation
        fields = ('id', 'sender_username', 'receiver_username')
