from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Profile

# Create your views here.

def profile(request, username):
	try:
		profile = Profile.objects.get(user=User.objects.get(username=username))
		return render(request, 'profile.html', {'profile': profile})
	except User.DoesNotExist or Profile.DoesNotExist:
		return render(request, 'not_found.html')