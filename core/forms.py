from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms

class UserSignupForm(UserCreationForm):
    GENDER_CHOICES = (
        ('male',   'Male'),
        ('female', 'Female'),
    )

    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        widget=forms.RadioSelect()
    )
    phone_number = forms.CharField(
        max_length=15,
        required=False
    )
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model  = User
        fields = [
            'first_name',
            'last_name',
            'gender',
            'phone_number',
            'email',
            'role',
            'password1',
            'password2'
        ]


class UserLoginForm(forms.Form):
    email    = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())