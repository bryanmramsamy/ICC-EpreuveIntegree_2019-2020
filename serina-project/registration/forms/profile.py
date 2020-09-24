from django import forms
from django.utils.translation import gettext_lazy as _


class UserProfileUpdateForm(forms.Form):
    """Form to update the user's profile."""

    first_name = forms.CharField(
        max_length=50,
        label=_("First name"),
        help_text=_("Your legal first name declared on your ID card."),
    )
    last_name = forms.CharField(
        max_length=50,
        label=_("Last name"),
        help_text=_("Your legal first name declared on your ID card."),
    )
    email = forms.EmailField(
        max_length=50,
        label=_("Contact e-mail address"),
        help_text=_("E-mail address on which you will receive notifications "
                    "and where our staff can contact you."),
    )


class StudentProfileUpdateForm(UserProfileUpdateForm):
    """Form to update the student's profile and StudentRegistrationReport's
    changeable data."""

    address = forms.CharField(
        max_length=255,
        label=_("Address"),
        help_text=_("Your legal residential address."),
    )
    additional_address = forms.CharField(
        required=False,
        max_length=255,
        label=_("Additional address"),
        help_text=_("Address complement for long addresses."),
    )
    postal_code = forms.CharField(
        max_length=50,
        label=_("Postal code"),
        help_text=_("Your legal residential postal code."),
    )
    postal_locality = forms.CharField(
        max_length=50,
        label=_("Locality"),
        help_text=_("Your legal residential postal locality designation."),
    )
