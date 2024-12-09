from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    USER_TYPE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    ]
    email = forms.EmailField(required=True, label="Email Address")
    identifier = forms.CharField(required=True, label="Identifier")
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, required=True, label="User Type")

    class Meta:
        model = CustomUser
        fields = ("username", "email", "identifier", "password1", "password2", "user_type")

class CustomUserLoginForm(forms.Form):
    identifier = forms.CharField(label="Identifier", max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
