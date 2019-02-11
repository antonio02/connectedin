from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import NewUserForm, UserLoginForm, ChangePasswordForm, DeactivateProfileForm
from django.views.generic.base import View
from django.contrib.auth.decorators import login_required
from .decorators import require_anon
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout as django_logout, update_session_auth_hash
from profiles.forms import NewProfileForm
from django.utils.translation import ugettext_lazy as _
from profiles.views import profile
from django.db import transaction


# Create your views here.

@login_required
def logout(request):
    django_logout(request)
    messages.success(request, _('Logout successfully'))
    return redirect('index')


class SignUpView(View):
    template_name = 'signup.html'

    def render_form(self, request):
        return render(request, self.template_name, {
            'profile_form': NewProfileForm(),
            'user_form': NewUserForm()
        })

    @method_decorator(require_anon)
    def get(self, request):
        return self.render_form(request)

    @transaction.atomic
    @method_decorator(require_anon)
    def post(self, request):
        profile_form = NewProfileForm(request.POST, request.FILES)
        user_form = NewUserForm(request.POST)

        if profile_form.is_valid() and user_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            messages.success(request, _('Account created'))
            return redirect('login')

        return render(request, self.template_name, {
            'profile_form': profile_form,
            'user_form': user_form
        })


class LoginView(View):
    template_name = 'login.html'

    @method_decorator(require_anon)
    def get(self, request):
        return render(request, self.template_name, {
            'login_form': UserLoginForm(),
        })

    @method_decorator(require_anon)
    def post(self, request):
        login_form = UserLoginForm(request.POST)

        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            login(request, user)
            if user.is_superuser:
                return redirect('admin_timeline')
            return redirect('index')

        return render(request, self.template_name, {
            'login_form': login_form,
        })


class ChangePasswordView(View):
    template_name = 'change_password.html'

    @method_decorator(login_required)
    def get(self, request):
        return render(request, self.template_name, {
            'change_form': ChangePasswordForm(),
        })

    @transaction.atomic
    @method_decorator(login_required)
    def post(self, request):
        change_form = ChangePasswordForm(request.POST)
        user = request.user
        if change_form.is_valid():
            if user.check_password(change_form.cleaned_data['old_password']):
                user.set_password(change_form.cleaned_data['password'])
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, _('Your password was changed'))
                return redirect(profile, username=user.username)
            else:
                change_form.add_error('old_password', _('Old password is incorrect'))
                return render(request, self.template_name, {
                    'change_form': change_form,
                })

        if not user.check_password(change_form.cleaned_data['old_password']):
            change_form.add_error('old_password', _('Old password is incorrect'))
        return render(request, self.template_name, {
            'change_form': change_form,
        })


class DeactivateProfileView(View):
    template_name = 'deactivate_profile.html'

    @method_decorator(login_required)
    def get(self, request):
        return render(request, self.template_name, {
            'deactivate_form': DeactivateProfileForm(),
        })

    @transaction.atomic
    @method_decorator(login_required)
    def post(self, request):
        deactivate_form = DeactivateProfileForm(request.POST)
        if deactivate_form.is_valid():
            request.user.is_active = False
            request.user.save()
            django_logout(request)
            messages.success(request, _('Your profile was deactivated'))
            return redirect('login')
        else:
            return render(request, self.template_name, {
                'deactivate_form': deactivate_form,
            })


class ActivateProfileView(View):
    template_name = 'activate_profile.html'

    @method_decorator(login_required)
    def get(self, request):
        return render(request, self.template_name)

    @transaction.atomic
    @method_decorator(login_required)
    def post(self, request):
        request.user.is_active = True
        request.user.save()
        messages.success(request, _('Your profile is now reactivated'))
        return redirect('index')

