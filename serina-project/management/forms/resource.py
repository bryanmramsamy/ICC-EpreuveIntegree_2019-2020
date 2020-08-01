from django import forms


class BackOfficeResourceFormMixin(forms.ModelForm):
    """Mixin for ModelForms thats hide the 'created_by' field and exclude the
    'reference' field if it exist."""

    class Meta:
        """Meta definition for BackOfficeResourceFormMixin."""

        exclude = ("reference",)
        widgets = {
            'created_by': forms.HiddenInput(),
        }
