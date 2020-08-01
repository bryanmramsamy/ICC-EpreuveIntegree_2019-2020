from django import forms
from django.conf import settings
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

    first_name = forms.CharField(label=_("First name"), required=True)
    last_name = forms.CharField(label=_("Last name"), required=True)
    email = forms.EmailField(
        label=_("Email"),
        required=True,
        error_messages={
            'invalid': _("Mail address invalid. Check the spelling or try "
                         "another one.")
        }
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

    def clean(self):
        """Check if the email is not already used by another user and check if
        the password and password confirmation match together.

        Raise an error with a displayed error message if one of these
        conditions failed.
        """

        cleaned_data = super(RegistrationForm, self).clean()

        email = cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_(
                "The entered mail address is already in use. Please use "
                "another one or contact our support team ({})."
                .format(settings.CONTACT_MAILS["support"])
                # TODO: Add clickable mailto link
            ))

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError(_(
                "Your password and your password confirmation does not match. "
                "Please try again."
            ))


class CustomAuthenticationForm(AuthenticationForm):
    """Custom AuthenticationForm supporting i18n."""

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
