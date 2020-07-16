from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    UserCreationForm
)
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _


class CustomUserCreationForm(UserCreationForm):
    """Customized UserCreationForm."""

    class Meta:
        """Meta definition of CustomUserCreationForm"""

        model = User
        fields = '__all__'


class CustomAuthenticationForm(AuthenticationForm):
    """Custom Authentication Form supporting i18n"""

    username = forms.CharField(
        label=_('Username'),
        widget=forms.TextInput(attrs={'autofocus': True})
    )

    password = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput()
    )


class CustomPasswordChangeForm(PasswordChangeForm):
    """Custom Authentication Form supporting i18n"""

    old_password = forms.CharField(
        label=_('Old password'),
        widget=forms.PasswordInput(attrs={'autofocus': True})
    )

    new_password1 = forms.CharField(
        label=_('New password'),
        widget=forms.PasswordInput()
    )

    new_password2 = forms.CharField(
        label=_('New password confirmation'),
        widget=forms.PasswordInput()
    )


class CustomPasswordResetForm(PasswordResetForm):
    """Custom PasswordResetForm supporting i18n"""

    email = forms.EmailField(
        label=_('Email address')
    )
