
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class UserForm(UserCreationForm):
    
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'type': 'username',
            'placeholder':('Username')
        }
    ))

    email = forms.EmailField(widget=forms.TextInput(
        attrs={
            'type':'email',
            'placeholder':('Email')
        }
    ))
    password1 = forms.CharField(max_length=16,widget=forms.PasswordInput(
        attrs={
            # 'class':'form-control',
            'placeholder':'Password'
        }
    ))
    password2 = forms.CharField(max_length=16,widget=forms.PasswordInput(
        attrs={
            # 'class':'form-control',
            'placeholder':'Repeat Password'
        }
    ))

    class Meta:
        model = User
        fields = ['username','email', 'password1','password2']
