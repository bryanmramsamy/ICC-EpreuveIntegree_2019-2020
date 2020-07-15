from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm
)
from django.utils.translation import ugettext as _


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

    