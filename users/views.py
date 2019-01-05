from django.shortcuts import render, redirect
from .forms import NewUserForm, UserLoginForm
from django.views.generic.base import View
from django.contrib.auth.decorators import login_required
from .decorators import require_anon
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout as django_logout
from django.contrib.auth.models import User
from profiles.forms import NewProfileForm

# Create your views here.

def index(request):
    return render(request, 'index.html')

@login_required
def logout(request):
	django_logout(request)
	return redirect(index)

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