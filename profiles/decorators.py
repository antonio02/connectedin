from .models import Profile
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

def profile_exist(func):
    def decorator(request, username, profile=None, *args, **kwargs):
        if profile is None:
            try:
                profile = Profile.objects.get(user__username=username)
                return func(request, username, profile=profile, *args, **kwargs)
            except Profile.DoesNotExist:
                return HttpResponse(status=404)
        else:
            return func(request, username, profile=profile, *args, **kwargs)

    return decorator

def require_other_profile(func):
    def decorator(request, username, *args, **kwargs):
        if request.user.username == username:
            return HttpResponse(status=400)
        return func(request, username, *args, **kwargs)

    return decorator


def profile_exist_and_not_blocked(func):

    @login_required
    @profile_exist
    def decorator(request, username, profile=None, user_profile=None, *args, **kwargs):
        if user_profile is None:
            user_profile = Profile.objects.get(user=request.user)
            if user_profile.blocked_contacts.filter(user__username=username).exists():
                return HttpResponse(status=404)
        else:
            if user_profile.blocked_contacts.filter(user__username=username).exists():
                return HttpResponse(status=404)
        
        if profile is None:
            profile = Profile.objects.get(user__username=username)
            if profile.blocked_contacts.filter(user__username=request.user.username).exists():
                return HttpResponse(status=404)
        else:
            if profile.blocked_contacts.filter(user__username=request.user.username).exists():
                return HttpResponse(status=404)
        
        return func(request, username, profile=profile, user_profile=user_profile, *args, **kwargs)

    return decorator

