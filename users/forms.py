from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Profile
from django.utils.translation import ugettext_lazy as _
from datetime import date


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
            self.add_error('retype_password',
                forms.ValidationError(_('Passwords does not match'), code='password_not_match'))
        return super(NewUserForm, self).clean()

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()

        return user

class NewProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(NewProfileForm, self).__init__(*args, **kwargs)
        self.fields['date_of_birth'].label    = _('Date of birth')

    class Meta:
        model = Profile
        fields = [
            'date_of_birth',
        ]

        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type':'date', 'placeholder': 'Date of Birth'})
        }

    def clean_date_of_birth(self):

        date_of_birth   = self.cleaned_data['date_of_birth']
        today           = date.today()
        restrict_date   = today.replace(year=today.year - 13)

        if date_of_birth > restrict_date:
            raise forms.ValidationError(_('You must be over 13 years old'), code='age_restriction')
        return date_of_birth

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
    