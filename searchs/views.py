from django.shortcuts import render
from profiles.models import Profile
from django.db.models import Q

# Create your views here.

def search(request, key):
    profiles = Profile.objects.filter(user__username__istartswith=key).all()
    return render(request, 'search_results.html', {'profiles': profiles})
