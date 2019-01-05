from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from .models import Profile, Invitation
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

# Create your views here.

def profile(request, username):
	try:
		profile = Profile.objects.get(user=User.objects.get(username=username))
		if request.user.is_authenticated:
			user_profile = Profile.objects.get(user=request.user)
			friendship = 0
			if Invitation.objects.filter(sender=user_profile, receiver=profile).exists():
				friendship = 1
			elif Invitation.objects.filter(sender=profile, receiver=user_profile).exists():
				friendship = 2
			elif profile.contacts.filter(user=request.user).exists():
				friendship = 3
			return render(request, 'profile.html', {'profile': profile, 'friendship': friendship})

		return render(request, 'profile.html', {'profile': profile})
	except User.DoesNotExist or Profile.DoesNotExist:
		return render(request, 'not_found.html')

@login_required
def invite_profile(request, username):
	if request.user.username == username:
		return redirect(profile, username=username)
	try:
		receiver = Profile.objects.get(user=User.objects.get(username=username))
	except User.DoesNotExist:
		return render(request, 'not_found.html')
	
	if receiver.contacts.filter(user=request.user).exists():
		return redirect(profile, username=username)
	
	sender = Profile.objects.get(user=request.user)
	if (Invitation.objects.filter(
		Q(receiver=receiver, sender=sender) | Q(receiver=sender, sender=receiver)).exists()):
		return redirect(profile, username=username)
	else:
		Invitation.objects.create(sender=sender, receiver=receiver)
		return redirect(profile, username=username)
	