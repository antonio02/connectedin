from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Profile, Invitation
from django.db.models import Q
from .decorators import *
from django.db import transaction
from django.core.paginator import Paginator


# Create your views here.

@profile_exist_and_not_blocked
def profile(request, username, profile=None, user_profile=None):
    if profile is None:
        profile = Profile.objects.get(user=User.objects.get(username=username))

    posts = profile.posts.all()
    paginador = Paginator(posts, 10)
    page = request.GET.get('page')
    posts = paginador.get_page(page)

    if request.user.is_authenticated:
        if request.user.username == username:
            return render(request, 'profile.html', {'profile': profile, 'posts': posts})

        friendship = 0
        invitation = None
        try:
            invitation = Invitation.objects.get(
                Q(sender__user__username=request.user.username,
                  receiver__user__username=username) |
                Q(sender__user__username=username,
                  receiver__user__username=request.user.username))
        except Invitation.DoesNotExist:
            pass

        if invitation is not None:
            if invitation.sender.user == request.user:
                friendship = 1
            if invitation.sender.user == profile.user:
                friendship = 2
        elif profile.contacts.filter(user=request.user).exists():
            friendship = 3

        return render(request, 'profile.html', {'profile': profile,
                                                'friendship': friendship,
                                                'invitation': invitation,
                                                'posts': posts})

    return render(request, 'profile.html', {'profile': profile, 'posts': posts})


@login_required
@profile_exist_and_not_blocked
@require_other_profile
def invite_profile(request, username, profile=None, user_profile=None):
    if profile is None:
        profile = Profile.objects.get(user=User.objects.get(username=username))

    if profile.contacts.filter(user=request.user).exists():
        return HttpResponse(status=400)

    if user_profile is None:
        user_profile = Profile.objects.get(user=request.user)

    if (Invitation.objects.filter(
            Q(receiver=profile, sender=user_profile) | Q(receiver=user_profile, sender=profile)).exists()):
        return HttpResponse(status=400)
    else:
        Invitation.objects.create(sender=user_profile, receiver=profile)
        return HttpResponse(status=200)


@login_required
def accept_invitation(request, invitation_id):
    try:
        invitation = Invitation.objects.get(id=invitation_id, sender__user__is_active=True)
        if invitation.receiver.user == request.user:
            invitation.accept()
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=403)
    except Invitation.DoesNotExist:
        return HttpResponse(status=404)


@login_required
def decline_invitation(request, invitation_id):
    try:
        invitation = Invitation.objects.get(id=invitation_id, sender__user__is_active=True)
        if invitation.receiver.user == request.user:
            invitation.decline()
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=403)
    except Invitation.DoesNotExist:
        return HttpResponse(status=404)


@login_required
def cancel_invitation(request, invitation_id):
    try:
        invitation = Invitation.objects.get(id=invitation_id, receiver__user__is_active=True)
        if invitation.sender.user == request.user:
            invitation.cancel()
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=403)
    except Invitation.DoesNotExist:
        return HttpResponse(status=404)


@transaction.atomic
@login_required
@require_other_profile
def remove_contact(request, username):
    try:
        user_profile = Profile.objects.get(user=request.user)
        remove_profile = user_profile.contacts.get(user__username=username, user__is_active=True)
        user_profile.contacts.remove(remove_profile)
        remove_profile.contacts.remove(user_profile)
        return HttpResponse(status=200)
    except User.DoesNotExist:
        return HttpResponse(status=404)
    except Profile.DoesNotExist:
        return HttpResponse(status=404)


@login_required
@require_other_profile
def give_super(request, username):
    if not request.user.is_superuser:
        return HttpResponse(status=403)

    try:
        user = User.objects.get(username=username)
        user.is_superuser = True
        user.save()
        return HttpResponse(status=200)

    except User.DoesNotExist:
        return HttpResponse(status=404)


@transaction.atomic
@login_required
@require_other_profile
@profile_exist_and_not_blocked
def block_profile(request, username, profile=None, user_profile=None):
    if profile is None:
        profile = Profile.objects.get(user__username=username)

    if profile.user.is_superuser:
        return HttpResponse(status=400)

    if user_profile is None:
        user_profile = Profile.objects.get(user__username=request.user.username)

    if user_profile.blocked_contacts.filter(user__username=username).exists():
        return HttpResponse(status=400)

    user_profile.blocked_contacts.add(profile)
    Invitation.objects.filter(
        Q(receiver=profile, sender=user_profile) | Q(receiver=user_profile, sender=profile)).delete()
    return redirect('index')


@login_required
@require_other_profile
@profile_exist_and_is_active
def unblock_profile(request, username, profile=None):
    if profile is None:
        profile = Profile.objects.get(user__username=username)

    user_profile = Profile.objects.get(user__username=request.user.username)

    if not user_profile.blocked_contacts.filter(user__username=username).exists():
        return HttpResponse(status=400)

    user_profile.blocked_contacts.remove(profile)
    return HttpResponse(status=200)
