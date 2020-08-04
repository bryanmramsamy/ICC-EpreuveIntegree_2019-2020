from django import forms

from ..models import (
    DegreeRegistrationReport,
    ModuleRegistrationReport,
    StudentRegistrationReport,
)
from ..utils.mixins import (
    HideCreatedByFieldFormMixin,
    VerboseDegreeModuleChoiceField,
)
from management.models import Degree, Module

# TODO: Comment correctly

class StudentRegistrationReportCreateFrom(HideCreatedByFieldFormMixin):
    """ModelForm for Module."""

    class Meta(HideCreatedByFieldFormMixin.Meta):
        """Meta definition for ModuleLevelForm."""

        model = StudentRegistrationReport
        fields = "__all__"


class ModuleRegistrationReportCreateFrom(forms.ModelForm):
    """ModelForm for Module."""

    module = VerboseDegreeModuleChoiceField(queryset=Module.objects.all(),
                                            empty_label=None)

    class Meta:
        """Meta definition for ModuleLevelForm."""

        model = ModuleRegistrationReport
        fields = ("student_rr", "module", "notes")
        widgets = {
            'student_rr': forms.HiddenInput(),
        }


class DegreeRegistrationReportCreateFrom(forms.ModelForm):
    """ModelForm for Module."""

    degree = VerboseDegreeModuleChoiceField(queryset=Degree.objects.all(),
                                            empty_label=None)

    class Meta:
        """Meta definition for ModuleLevelForm."""

        model = DegreeRegistrationReport
        fields = ("student_rr", "degree", "notes")
        widgets = {
            'student_rr': forms.HiddenInput(),
        }
