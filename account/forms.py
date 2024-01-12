from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import *


from django.db import models

# from django.contrib.auth.models import User
import datetime as dt
from django.forms import CharField, ModelForm
from django.urls import reverse
# from account.models import Profile


# from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, UserChangeForm
# from django.contrib.auth.models import User
from .models import UserProfuile
# from .models import Wallet
from . import models


class DepositForm(forms.ModelForm):
    deposited_amount = forms.DecimalField(widget=forms.TextInput(attrs={'type': 'number'}))

    class Meta:
        model = Wallet
        fields = ['deposited_amount']

    def clean_amount(self):
        amount = self.cleaned_data['deposited_amount']
        # Add any additional validation for the amount if needed
        return deposited_amount



class SignUpForm(UserCreationForm):
    name = forms.CharField(label=("Full Name"))
    username = forms.EmailField(label=("Email"))
    phone_number = forms.CharField(label=("Phone Number"), required=False)
    profile_picture = forms.ImageField(label=("Profile Picture"), required=False)

    class Meta:
        model = User
        fields = ('name', 'username', 'phone_number', 'profile_picture', 'password1', 'password2')


class UserPublicDetailsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['user'].widget.attrs.update({
            'hidden': "hidden"
        })
        
        self.fields['user'].widget.attrs.update({
            'hidden': "hidden"
        })

        self.fields['bio'].widget.attrs.update({
            "rows": "3"
        })

        self.fields['currently_hacking_on'].widget.attrs.update({
            "rows": "2"
        })

        self.fields['currently_learning'].widget.attrs.update({
            "rows": "2"
        })

        self.fields['skills_language'].widget.attrs.update({
            "rows": "2",
            "placeholder": "eg: django, python, java, javascript"
        })

        self.fields['education'].widget.attrs.update({
            "rows": "3"
        })
        self.fields['work'].widget.attrs.update({
            "rows": "3"
        })

    class Meta:
        model = UserProfuile
        fields = "__all__"

class LoginUserForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your username'
        })
        
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your password'
        })
    class Meta:
        fields = ['username', 'password']

class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your username'
        })

        self.fields['first_name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your first name'
        })

        self.fields['last_name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your last name'
        })

        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your email-id'
        })

        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm your password'
        })
    username = forms.CharField(max_length=150)
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField(max_length=150)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        
        
class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Old Password'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New Passowrd'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Conform new password'}))
    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']
        
        
class EditUserProfileForm(UserChangeForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': "Enter uour username"}))
    
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Enter your first name"}))

    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Enter your last name"}))

    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Enter your last name"}))
    class Meta:
        model = User
        fields = ['username', 'first_name', "last_name", 'email']

