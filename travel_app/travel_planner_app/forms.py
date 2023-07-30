# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Review

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields =['username', 'password1', 'password2', 'email','first_name','last_name']

class ReviewForm(forms.ModelForm):
    
    class Meta:
        model = Review
        fields = '__all__'
