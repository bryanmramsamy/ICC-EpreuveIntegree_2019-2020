from django import forms

from ..models import ModuleRegistrationReport


class PaymentForm(forms.Form):
    """PaymentForm definition."""

    module_rr = forms.ModelChoiceField(
        queryset=ModuleRegistrationReport.objects.all(),
        empty_label=None,
    )
