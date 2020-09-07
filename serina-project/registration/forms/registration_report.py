from django import forms
from django.utils.translation import gettext_lazy as _

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


class StudentRegistrationReportCreateFrom(HideCreatedByFieldFormMixin):
    """StudentRegistrationReport creation form with hidden (and autofilled in
    the views) 'created_by field."""

    class Meta(HideCreatedByFieldFormMixin.Meta):
        """Meta definition for StudentRegistrationReportCreateFrom."""

        model = StudentRegistrationReport
        fields = "__all__"
        labels = {
            "id_picture": _("Your ID photo"),
            "id_card": _("Scan of your ID card"),
            "notes": _("Additional notes you would like to add")
        }


class ModuleRegistrationReportCreateFrom(forms.ModelForm):
    """ModelForm for Module."""  # TODO: Comment correctly

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
    """ModelForm for Module."""  # TODO: Comment correctly

    degree = VerboseDegreeModuleChoiceField(queryset=Degree.objects.all(),
                                            empty_label=None)

    class Meta:
        """Meta definition for ModuleLevelForm."""

        model = DegreeRegistrationReport
        fields = ("student_rr", "degree", "notes")
        widgets = {
            'student_rr': forms.HiddenInput(),
        }
