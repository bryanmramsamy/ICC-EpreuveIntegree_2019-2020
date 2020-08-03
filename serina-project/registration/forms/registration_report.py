from django import forms

from ..models import ModuleRegistrationReport, StudentRegistrationReport
from ..utils.mixins import (
    HideCreatedByFieldFormMixin,
    VerboseModuleChoiceField,
)
from management.models import Module


class StudentRegistrationReportCreateFrom(HideCreatedByFieldFormMixin):
    """ModelForm for Module."""

    class Meta(HideCreatedByFieldFormMixin.Meta):
        """Meta definition for ModuleLevelForm."""

        model = StudentRegistrationReport
        fields = "__all__"


class ModuleRegistrationReportCreateFrom(forms.ModelForm):
    """ModelForm for Module."""

    module = VerboseModuleChoiceField(queryset=Module.objects.all(),
                                      empty_label=None)

    class Meta:
        """Meta definition for ModuleLevelForm."""

        model = ModuleRegistrationReport
        fields = ("student_rr", "module",)
        widgets = {
            'student_rr': forms.HiddenInput(),
        }
