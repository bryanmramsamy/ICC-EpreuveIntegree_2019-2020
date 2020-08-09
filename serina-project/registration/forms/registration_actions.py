from django import forms
from django.utils.translation import ugettext as _


class SubmitFinalScoreForm(forms.Form):
    """Form to submit a final score to a ModuleRegistrationReport instance."""

    score = forms.DecimalField(
        min_value=0,
        max_value=100,
        decimal_places=2,
        label=_("Student's module final score"),
    )
