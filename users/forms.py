from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _


class NewUserForm(forms.ModelForm):
    retype_password = forms.CharField(required=True,
    widget=forms.PasswordInput(), max_length=128)

    def __init__(self, *args, **kwargs):
        super(NewUserForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required  = True
        self.fields['email'].required       = True

        self.fields['first_name'].label         = _('First name')
        self.fields['last_name'].label          = _('Last name')
        self.fields['username'].label           = _('Username')
        self.fields['email'].label              = _('Email')
        self.fields['password'].label           = _('Password')
        self.fields['retype_password'].label    = _('Confirm password')

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]

        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(_('Username "%(username)s" is already in use.'),
            params={'username': username}, code='username_in_use')
        return username
    
    def clean(self):

        if self.cleaned_data['password'] != self.cleaned_data['retype_password']:
            self.add_error('password',
                forms.ValidationError(''))
            self.add_error('retype_password',
                forms.ValidationError(_('Passwords does not match'), code='password_not_match'))
        return super(NewUserForm, self).clean()

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()

        return user

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].required  = True
        self.fields['password'].required  = True

        self.fields['username'].label  = _('Username')
        self.fields['password'].label  = _('Password')

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError(_('Wrong username or password'), code='wrong_login')
        
        return super(UserLoginForm, self).clean()

class ChangePasswordForm(forms.Form):
    old_password    = forms.CharField(widget=forms.PasswordInput, required=True, max_length=128)
    password        = forms.CharField(widget=forms.PasswordInput, required=True, max_length=128)
    retype_password = forms.CharField(widget=forms.PasswordInput, required=True, max_length=128)

    
    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

        self.fields['old_password'].label   = _('Old Password')
        self.fields['password'].label       = _('New password')
        self.fields['retype_password'].label= _('Confirm password')

    def clean(self):

        if self.cleaned_data['password'] != self.cleaned_data['retype_password']:
            self.add_error('password',
                forms.ValidationError(''))
            self.add_error('retype_password',
                forms.ValidationError(_('Passwords does not match'), code='password_not_match'))
        return super(ChangePasswordForm, self).clean()
