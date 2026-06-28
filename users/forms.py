from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

from .models import User


def validate_github_url(github_url):
    if github_url and "github.com" not in github_url:
        raise ValidationError("Ссылка должна вести на GitHub")
    return github_url


class RegisterForm(forms.ModelForm):
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["name", "surname", "email", "password"]

    def clean_email(self):
        return self.cleaned_data["email"].lower()

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        if email and password:
            user = authenticate(email=email, password=password)
            if user is None:
                raise ValidationError("Неверный email или пароль")
            cleaned_data["user"] = user
        return cleaned_data


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["avatar", "name", "surname", "about", "phone", "github_url"]

    def clean_github_url(self):
        return validate_github_url(self.cleaned_data.get("github_url"))
