from django import forms
from .models import Profile
from datetime import date
from django.utils.translation import ugettext_lazy as _

class NewProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(NewProfileForm, self).__init__(*args, **kwargs)
        self.fields['date_of_birth'].label    = _('Date of birth')

    class Meta:
        model = Profile
        fields = [
            'date_of_birth', 'photo'
        ]

        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'placeholder': 'Date of Birth'}),
            'photo': forms.FileInput(attrs={'class': 'border rounded', 'style': 'width: 150px;height: 150px;object-fit: cover;'})
        }

    def clean_date_of_birth(self):

        date_of_birth   = self.cleaned_data['date_of_birth']
        today           = date.today()
        restrict_date   = today.replace(year=today.year - 13)

        if date_of_birth > restrict_date:
            raise forms.ValidationError(_('You must be over 13 years old'), code='age_restriction')
        return date_of_birth
