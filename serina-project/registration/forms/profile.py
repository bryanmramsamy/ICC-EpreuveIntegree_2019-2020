from django import forms


class UserProfileUpdateForm(forms.Form):
    """Form to update the user's profile."""

    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=50)


class StudentProfileUpdateForm(UserProfileUpdateForm):
    """Form to update the student's profile and StudentRegistrationReport's
    changeable data."""

    nationality = forms.CharField(max_length=50)
    address = forms.CharField(max_length=255)
    additional_address = forms.CharField(max_length=255)
    postal_code = forms.CharField(max_length=50)
    postal_locality = forms.CharField(max_length=50)
