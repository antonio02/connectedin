from django.shortcuts import render
from profiles.models import Profile
from django.db.models import Q


# Create your views here.

def search(request, key=None):
    if key:
        if request.user.is_authenticated:
            user_profile = Profile.objects.get(user__username=request.user.username)
            blocked_usernames = [i.user.username for i in user_profile.blocked_contacts.all()]
            profiles = Profile.objects.filter(Q(user__username__istartswith=key) |
                                              Q(user__first_name__istartswith=key) |
                                              Q(user__last_name__istartswith=key),
                                              ~Q(blocked_contacts__user=request.user),
                                              ~Q(user__username__in=blocked_usernames)).all()
            return render(request, 'search_results.html', {'profiles': profiles,
                                                           'user_profile': user_profile})
        else:
            profiles = Profile.objects.filter(Q(user__username__istartswith=key) |
                                              Q(user__first_name__istartswith=key) | Q(
                user__last_name__istartswith=key)).all()

        return render(request, 'search_results.html', {'profiles': profiles})

    return render(request, 'search_results.html', {'profiles': None})
