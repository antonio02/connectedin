from django.urls import path
from .views import *

urlpatterns = [
    path('<str:username>/', profile, name='profile'),
    path('<str:username>/invite/', invite_profile, name='invite_profile'),
    path('<str:username>/remove/', remove_contact, name='remove_contact'),
    path('<str:username>/give_super/', give_super, name='give_super'),
    path('invitations/<int:invitation_id>/accept', accept_invitation, name='accept_invitation'),
    path('invitations/<int:invitation_id>/decline', decline_invitation, name='decline_invitation'),
    path('invitations/<int:invitation_id>/cancel', cancel_invitation, name='cancel_invitation'),
]