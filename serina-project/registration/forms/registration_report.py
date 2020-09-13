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


class ForeignStudentRegistrationReportCreateFrom(HideCreatedByFieldFormMixin):
    """StudentRegistrationReport creation form with hidden (and autofilled in
    the views) 'created_by field.

    Student Registration request form for foreign students.
    Foreign students must fill additional fields and send additional data which
    are not required for homegrown students.
    This form adds those fields.
    """

    class Meta(HideCreatedByFieldFormMixin.Meta):
        """Meta definition for StudentRegistrationReportCreateFrom."""

        model = StudentRegistrationReport
        fields = "__all__"
        labels = {
            "id_picture": _("Your ID photo"),
            "id_card": _("Scan of your ID card"),
            "notes": _("Additional notes you would like to add")
        }
        help_texts = {
            "id_picture": _("JPEG pictures only"),
            "id_card": _("JPEG scans or PDF files only"),
            "secondary_education_certificate": _(
                "Secondary education completion certificate or equivalent "
                "document."
            ),
            "archievement_certificates": _(
                "If you already succeeded one or more similar modules in "
                "another school, you can send your success certificates in a "
                "zip file. Our staff will decide if one or some certificates "
                "can grant you an exemption for one or some or our modules."
            ),
            "job_organization_certificates": _(
                "Any job certificates from organizations such as the 'VDAB', "
                "the 'CPAS', the 'PHARE' or any similar organization."
            ),
            "exemption_report": _(
                "Any of your academic reports which could lead to a potential "
                "exemption."
            ),
        }


class HomegrownStudentRegistrationReportCreateFrom(
    ForeignStudentRegistrationReportCreateFrom,
):
    """StudentRegistrationReport creation form with hidden (and autofilled in
    the views) 'created_by field.

    Student Registration request form for homegrown students.
    Homegrown students are exempted of filling some additional data which are
    mandatory for foreign students.
    This form ommit those fields."""

    class Meta(ForeignStudentRegistrationReportCreateFrom.Meta):
        """Meta definition for StudentRegistrationReportCreateFrom."""

        model = StudentRegistrationReport
        exclude = (
            "annex_403",
            "other_school_inscription_certificate",
            "national_register_extract",
            "belgian_studies_history",
        )


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
