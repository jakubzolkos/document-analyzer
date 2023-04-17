from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms

class UserForm(UserCreationForm):
    
    username = forms.CharField(required=False, widget=forms.HiddenInput())

    email = forms.EmailField(required=True, widget=forms.TextInput(
        attrs={
            'type':'email',
            'placeholder':('Email')
        }
    ))

    password1 = forms.CharField(max_length=16,widget=forms.PasswordInput(
        attrs={
            'placeholder':'Password'
        }
    ))
    
    password2 = forms.CharField(max_length=16,widget=forms.PasswordInput(
        attrs={
            'placeholder':'Repeat Password'
        }
    ))

    class Meta:
        model = User
        fields = ('email', 'password1','password2')
