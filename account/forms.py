from django.contrib.auth.forms import UserCreationForm
import re
from django import forms
from .models import User
from order.models import telephone_validator

class RegistrForm(UserCreationForm):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    email = forms.CharField(max_length=256)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'nbm', 'username',
                  'email', 'password1', 'password2']

    def clean_password(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError(
                ('Passwords don\'t match.'), code='Invalid')
        return cd['password2']

    def clean_email(self):
        cd = self.cleaned_data
        if cd['email'] in [it.email for it in User.objects.all()]:
            raise forms.ValidationError(
                ('User with this email is already registered'))
        return cd['email']


    def clean_nbm(self):
        cd = self.cleaned_data
        nbm = cd['nbm']

        return telephone_validator(nbm)
