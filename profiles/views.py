from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from posts.forms import CommentForm, SharePostForm
from .models import Profile, Invitation
from django.db.models import Q
from .decorators import *
from django.db import transaction
from django.core.paginator import Paginator
from django.utils.translation import ugettext_lazy as _


# Create your views here.

@profile_exist_and_not_blocked
def profile(request, username, profile=None, user_profile=None):
    if profile is None:
        profile = Profile.objects.get(user=User.objects.get(username=username))

    posts = profile.posts.order_by('-post_date').all()
    paginador = Paginator(posts, 10)
    page = request.GET.get('page')
    posts = paginador.get_page(page)

    if request.user.is_authenticated:
        if request.user.username == username:
            return render(request, 'profile.html', {'profile': profile,
                                                    'comment_form': CommentForm(),
                                                    'share_form': SharePostForm(),
                                                    'user_profile': Profile.objects.get(user=request.user),
                                                    'posts': posts})

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

        return render(request, 'profile.html', {'user_profile': Profile.objects.get(user=request.user),
                                                'comment_form': CommentForm(),
                                                'share_form': SharePostForm(),
                                                'profile': profile,
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
        messages.warning(request, _('Profile already in contacts'))
        return HttpResponse(status=400)

    if user_profile is None:
        user_profile = Profile.objects.get(user=request.user)

    if (Invitation.objects.filter(
            Q(receiver=profile, sender=user_profile) | Q(receiver=user_profile, sender=profile)).exists()):
        messages.warning(request, _('There is a pending invitation'))
        return HttpResponse(status=400)
    else:
        messages.success(request, _('Invitation sent'))
        Invitation.objects.create(sender=user_profile, receiver=profile)
        return HttpResponse(status=200)


@login_required
def accept_invitation(request, invitation_id):
    try:
        invitation = Invitation.objects.get(id=invitation_id, sender__user__is_active=True)
        if invitation.receiver.user == request.user:
            invitation.accept()
            messages.success(request, _('Invitation accepted'))
            return HttpResponse(status=200)
        else:
            messages.error(request, _('Invitation not found'))
            return HttpResponse(status=403)
    except Invitation.DoesNotExist:
        messages.error(request, _('Invitation not found'))
        return HttpResponse(status=404)


@login_required
def decline_invitation(request, invitation_id):
    try:
        invitation = Invitation.objects.get(id=invitation_id, sender__user__is_active=True)
        if invitation.receiver.user == request.user:
            invitation.decline()
            messages.success(request, _('Invitation declined'))
            return HttpResponse(status=200)
        else:
            messages.error(request, _('Invitation not found'))
            return HttpResponse(status=404)
    except Invitation.DoesNotExist:
        messages.error(request, _('Invitation not found'))
        return HttpResponse(status=404)


@login_required
def cancel_invitation(request, invitation_id):
    try:
        invitation = Invitation.objects.get(id=invitation_id, receiver__user__is_active=True)
        if invitation.sender.user == request.user:
            invitation.cancel()
            messages.success(request, _('Invitation canceled'))
            return HttpResponse(status=200)
        else:
            messages.error(request, _('Invitation not found'))
            return HttpResponse(status=404)
    except Invitation.DoesNotExist:
        messages.error(request, _('Invitation not found'))
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
        messages.success(request, _('%(first_name)s removed from contacts' % {'first_name': remove_profile.user.first_name}))
        return HttpResponse(status=200)
    except User.DoesNotExist:
        messages.error(request, _('Profile not found'))
        return HttpResponse(status=404)
    except Profile.DoesNotExist:
        messages.error(request, _('Profile not found'))
        return HttpResponse(status=404)


@login_required
@require_other_profile
def give_super(request, username):
    if not request.user.is_superuser:
        messages.error(request, _('You need to be a Admin'))
        return HttpResponse(status=403)

    try:
        user = User.objects.get(username=username)
        user.is_superuser = True
        user.save()
        messages.success(request, _('This profile is now a admin'))
        return HttpResponse(status=200)

    except User.DoesNotExist:
        messages.error(request, _('Profile not found'))
        return HttpResponse(status=404)


@transaction.atomic
@login_required
@require_other_profile
@profile_exist_and_not_blocked
def block_profile(request, username, profile=None, user_profile=None):
    if profile is None:
        profile = Profile.objects.get(user__username=username)

    if profile.user.is_superuser:
        messages.warning(request, _('You cannot block a admin'))
        return HttpResponse(status=400)

    if user_profile is None:
        user_profile = Profile.objects.get(user__username=request.user.username)

    if user_profile.blocked_contacts.filter(user__username=username).exists():
        messages.warning(request, _('You already blocked this profile'))
        return HttpResponse(status=400)

    user_profile.blocked_contacts.add(profile)
    Invitation.objects.filter(
        Q(receiver=profile, sender=user_profile) | Q(receiver=user_profile, sender=profile)).delete()
    messages.success(request, _('%(first_name)s blocked' % {'first_name': profile.user.first_name}))
    return redirect('index')


@login_required
@require_other_profile
@profile_exist_and_is_active
def unblock_profile(request, username, profile=None):
    if profile is None:
        profile = Profile.objects.get(user__username=username)

    user_profile = Profile.objects.get(user__username=request.user.username)

    if not user_profile.blocked_contacts.filter(user__username=username).exists():
        messages.warning(request, _('This profile is not blocked'))
        return HttpResponse(status=400)

    user_profile.blocked_contacts.remove(profile)
    messages.success(request, _('%(first_name)s unblocked' % {'first_name': profile.user.first_name}))
    return HttpResponse(status=200)
