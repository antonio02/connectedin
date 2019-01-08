from django.shortcuts import render, redirect
from .forms import NewUserForm, UserLoginForm, ChangePasswordForm
from django.views.generic.base import View
from django.contrib.auth.decorators import login_required
from .decorators import require_anon
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout as django_logout, update_session_auth_hash
from django.contrib.auth.models import User
from profiles.forms import NewProfileForm
from django.utils.translation import ugettext_lazy as _
from profiles.views import profile

# Create your views here.

@login_required
def logout(request):
	django_logout(request)
	return redirect('index')

class SignUpView(View):

	template_name = 'signup.html'
	
	def render_form(self, request):
		return render(request, self.template_name, {
			'profile_form'	: NewProfileForm(),
			'user_form'	    : NewUserForm()
			})

	@method_decorator(require_anon)
	def get(self, request):
		return self.render_form(request)

	@method_decorator(require_anon)
	def post(self, request):
		profile_form 	= NewProfileForm(request.POST)
		user_form 	    = NewUserForm(request.POST)

		if profile_form.is_valid() and user_form.is_valid():

			user 		    = user_form.save()
			profile 		= profile_form.save(commit=False)
			profile.user    = user
			profile.save()

			return redirect('login')

		return render(request, self.template_name, {
			'profile_form'	: profile_form,
			'user_form'	    : user_form
			})

class LoginView(View):

	template_name = 'login.html'

	@method_decorator(require_anon)
	def get(self, request):
		return render(request, self.template_name, {
			'login_form'	: UserLoginForm(),
			})

	@method_decorator(require_anon)
	def post(self, request):
		login_form = UserLoginForm(request.POST)

		if login_form.is_valid():
			username = login_form.cleaned_data['username']
			password = login_form.cleaned_data['password']
			user = authenticate(username=username, password=password)
			login(request, user)
			return redirect('index')
		
		return render(request, self.template_name, {
			'login_form'	: login_form,
			})

class ChangePasswordView(View):

	template_name = 'change_password.html'

	@method_decorator(login_required)
	def get(self, request):
		return render(request, self.template_name, {
			'change_form'	: ChangePasswordForm(),
			})

	@method_decorator(login_required)
	def post(self, request):
		change_form = ChangePasswordForm(request.POST)
		user = request.user
		if change_form.is_valid():
			if user.check_password(change_form.cleaned_data['old_password']):
				user.set_password(change_form.cleaned_data['password'])
				user.save()
				update_session_auth_hash(request, user)
				return redirect(profile, username=user.username)
			else:
				change_form.add_error('old_password', _('Old password is incorrect'))
				return render(request, self.template_name, {
				'change_form'	: change_form,
				})

		if not user.check_password(change_form.cleaned_data['old_password']):
			change_form.add_error('old_password', _('Old password is incorrect'))
		return render(request, self.template_name, {
			'change_form'	: change_form,
			})