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
			if request.user.username == username:
				return render(request, 'profile.html', {'profile': profile})

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
			'invitation': invitation})

		return render(request, 'profile.html', {'profile': profile})
	except User.DoesNotExist:
		return render(request, 'not_found.html')

@login_required
def invite_profile(request, username):
	if request.user.username == username:
		return HttpResponse(status=400)
	try:
		receiver = Profile.objects.get(user=User.objects.get(username=username))
	except User.DoesNotExist:
		return HttpResponse(status=404)
	
	if receiver.contacts.filter(user=request.user).exists():
		return HttpResponse(status=400)
	
	sender = Profile.objects.get(user=request.user)
	if (Invitation.objects.filter(
		Q(receiver=receiver, sender=sender) | Q(receiver=sender, sender=receiver)).exists()):
		return HttpResponse(status=400)
	else:
		Invitation.objects.create(sender=sender, receiver=receiver)
		return HttpResponse(status=200)
	
@login_required
def accept_invitation(request, invitation_id):
	try:
		invitation = Invitation.objects.get(id=invitation_id)
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
		invitation = Invitation.objects.get(id=invitation_id)
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
		invitation = Invitation.objects.get(id=invitation_id)
		if invitation.sender.user == request.user:
			invitation.cancel()
			return HttpResponse(status=200)
		else:
			return HttpResponse(status=403)
	except Invitation.DoesNotExist:
		return HttpResponse(status=404)

@login_required
def remove_contact(request, username):
	if request.user.username == username:
		return HttpResponse(status=400)
	try:
		user_profile 	= Profile.objects.get(user=request.user)
		remove_profile 	= user_profile.contacts.get(user__username=username)
		user_profile.contacts.remove(remove_profile)
		remove_profile.contacts.remove(user_profile)
		return HttpResponse(status=200)
	except User.DoesNotExist:
		return HttpResponse(status=404)
	except Profile.DoesNotExist:
		return HttpResponse(status=404)

@login_required
def give_super(request, username):
	if request.user.username == username:
		return HttpResponse(status=400)
	
	if not request.user.is_superuser:
		return HttpResponse(status=403)

	try:
		user = User.objects.get(username=username)
		user.is_superuser = True
		user.save()
		return HttpResponse(status=200)

	except User.DoesNotExist:
		return HttpResponse(status=404)