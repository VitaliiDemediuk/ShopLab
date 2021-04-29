from django import forms
from django.contrib.auth.forms import AuthenticationForm
from shop.forms.forms import CustomUserCreationForm
from shop.models import CustomUser


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class RegistrationForm(CustomUserCreationForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="Password confirmation:", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'password1', 'password2')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'autofocus': 'autofocus'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

class ResetPasswordForm(forms.Form):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="Password confirmation:", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
