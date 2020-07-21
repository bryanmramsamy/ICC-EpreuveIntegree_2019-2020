from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    UserCreationForm
)
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _


class RegistrationForm(forms.Form):
    """Customized UserCreationForm."""

    first_name = forms.CharField(
        label=_("First name"),
        required=True,
    )
    last_name = forms.CharField(
        label=_("Last name"),
        required=True,
    )
    email = forms.EmailField(
        label=_("Email"),
        required=True,
    )
    password = forms.CharField(
        label=_("Password"),
        required=True,
        widget=forms.PasswordInput
    )
    confirm_password = forms.CharField(
        label=_("Password confirmation"),
        required=True,
        widget=forms.PasswordInput
    )
    birthday = forms.DateField(
        label=_('Birthday date'),
        required=True,
    )
    nationality = forms.CharField(
        label=_('Nationality'),
        required=True,
    )
    address = forms.CharField(
        label=_('Address'),
        required=True,
    )
    postalCode = forms.CharField(
        label=_('Postal code'),
        required=True,
    )
    postalLocality = forms.CharField(
        label=_('Locality'),
        required=True,
    )


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
