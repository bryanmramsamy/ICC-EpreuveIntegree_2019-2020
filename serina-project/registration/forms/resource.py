from django import forms


class FrontOfficeResourceFormMixin(forms.ModelForm):
    """Mixin for ModelForms thats hide the 'created_by' field."""

    class Meta:
        """Meta definition for FrontOfficeResourceFormMixin."""

        widgets = {
            'created_by': forms.HiddenInput(),
        }
