# forms.py
from django import forms
from .models import ExternalUser

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = ExternalUser
        fields = ['email', 'username', 'password']
