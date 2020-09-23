from django import forms
from django.utils.translation import gettext as _


class SubmitFinalScoreForm(forms.Form):
    """Form to submit a final score to a ModuleRegistrationReport instance."""

    final_score = forms.DecimalField(
        min_value=0,
        max_value=100,
        decimal_places=2,
        label=_("Student's module final score"),
        help_text=(_("Student's final score on this module. This score will "
                     "determine if the student succeeded the module or not.")),
    )
    notes = forms.CharField(
        widget=forms.Textarea,
        label=_("Additonal notes"),
        help_text=(_("Additional notes from the staff or the teachers.")),
    )
