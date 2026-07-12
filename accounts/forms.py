from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
import re


class LoginForm(AuthenticationForm):

    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter Username",
                "autocomplete": "username",
            }
        ),
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter Password",
                "autocomplete": "current-password",
            }
        ),
    )

    def clean_username(self):
        username = self.cleaned_data.get("username", "").strip()

        if not username:
            raise ValidationError("Username is required.")

        if len(username) < 3:
            raise ValidationError("Username must contain at least 3 characters.")

        if not re.match(r"^[A-Za-z0-9_.@]+$", username):
            raise ValidationError(
                "Username can contain only letters, numbers, ., _, and @."
            )

        return username

    def clean_password(self):
        password = self.cleaned_data.get("password")

        if not password:
            raise ValidationError("Password is required.")

        if len(password) < 8:
            raise ValidationError("Password must contain at least 8 characters.")

        return password