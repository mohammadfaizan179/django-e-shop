from django.contrib.auth import password_validation
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm, UserCreationForm,AuthenticationForm, UsernameField, PasswordChangeForm
from django.contrib.auth.models import User
from django import forms
from django.db.models import fields
from django.forms import widgets
from django.utils.translation import gettext, gettext_lazy as _   
from app import models
from .models import Customer

class UserRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Password Confirm', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    email = forms.EmailField(label='Email',required=True, widget=forms.EmailInput(attrs={'class':'form-control'}))
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control'}),
            'first_name': forms.TextInput(attrs={'class':'form-control'}),
            'last_name': forms.TextInput(attrs={'class':'form-control'}),
        }

class UserLoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus':True, 'class':'form-control'}))
    password = forms.CharField(label=_('Password'), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'class':'form-control'}))
    
    
class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label=_('Old Password'), strip =False, widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'autofocus':True ,'class':'form-control'}))
    new_password1 = forms.CharField(label=_('New Password'), strip =False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password', 'autofocus':True ,'class':'form-control'}), help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_('Confirm New Password'), strip =False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password', 'class':'form-control'}))

class UserPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label=_('Email'), max_length=254, widget=forms.EmailInput(attrs={'autocomplete':'email', 'class':'form-control'}))

class UserResetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label=_('New Password'), strip =False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password', 'autofocus':True ,'class':'form-control'}), help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_('Confirm New Password'), strip =False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password', 'class':'form-control'}))

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name','locality','city','state','zipcode']
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}), 
            'locality': forms.TextInput(attrs={'class':'form-control'}), 
            'city': forms.TextInput(attrs={'class':'form-control'}), 
            'state': forms.Select(attrs={'class':'form-control'}), 
            'zipcode': forms.NumberInput(attrs={'class':'form-control'}), 
        }