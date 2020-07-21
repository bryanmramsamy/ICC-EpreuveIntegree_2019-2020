from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    UserCreationForm
)
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _


class RegistrationForm(forms.ModelForm):
    """Customized UserCreationForm."""

    confirm_password = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput
    )

    birthday = forms.DateField(
        label=_('Birthday date'),
    )

    nationality = forms.CharField(
        label=_('Nationality')
    )

    address = forms.CharField(
        label=_('Address')
    )

    postalCode = forms.CharField(
        label=_('Postal code')
    )

    postalLocality = forms.CharField(
        label=_('Locality')
    )

    class Meta:
        """Meta definition of CustomUserCreationForm"""

        model = User
        fields = {
            'first_name',
            'last_name',
            'email',
            'password',
        }

        labels = {
            'password1': _('Password'),
            'password2': _('Password confirmation'),
            'email': _('Email'),
            'first_name': _('First name'),
            'last_name': _('Last name')
        }

    def __init__(self, *args, **kwargs):
        """Make email, first_name and last_name fields required."""

        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True


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
