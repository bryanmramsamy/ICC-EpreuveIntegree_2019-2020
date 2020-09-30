from django import forms

from .models import StudentRating
from management.models import Degree, Module
from registration.utils import mixins as mixins_utils


class StudentRatingForm(mixins_utils.HideCreatedByFieldFormMixin):
    """ModelForm for StudentRating."""

    module = mixins_utils.VerboseDegreeModuleChoiceField(
        queryset=Module.objects.all(),
        required=False,
        widget=forms.HiddenInput()
    )
    degree = mixins_utils.VerboseDegreeModuleChoiceField(
        queryset=Degree.objects.all(),
        required=False,
        widget=forms.HiddenInput()
    )

    class Meta(mixins_utils.HideCreatedByFieldFormMixin.Meta):
        """Meta definition for StudentRegistrationForm."""

        model = StudentRating
        exclude = ("is_visible",)
