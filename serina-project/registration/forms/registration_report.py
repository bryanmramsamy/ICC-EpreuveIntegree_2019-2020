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
    the views) 'created_by field.
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
            "secondary_education_certificate": _(
                "Secondary education completion certificate or equivalent "
                "document."
            ),
            "student_is_foreigner": _(
                "Check this if you are a foreign student. If you are, you "
                "must fill additional fields."
            ),
            "annex_403": _("Circular annex 403 for social promotion studies."),
            "other_school_inscription_certificate": _(
                "Other school registration certificate for 60 ECTS."
            ),
            "national_register_extract": _(""),
            "belgian_studies_history": _(""),
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


class ModuleRegistrationReportCreateFrom(forms.ModelForm):
    """ModelForm for ModuleRegistrationReportCreateFrom.

    All the fields are hidden and autocompleted by the view.
    """

    class Meta:
        """Meta definition for ModuleLevelForm."""

        model = ModuleRegistrationReport
        fields = (
            "student_rr",
            "module",
            "exemption_request",
            "exemption_report",
            "notes"
        )
        widgets = {
            'student_rr': forms.HiddenInput(),
            'module': forms.HiddenInput(),
            'notes': forms.HiddenInput(),
        }


class DegreeRegistrationReportCreateFrom(forms.ModelForm):
    """ModelForm for DegreeRegistrationReportCreateFrom.

    All the fields are hidden and autocompleted by the view.
    """

    class Meta:
        """Meta definition for ModuleLevelForm."""

        model = DegreeRegistrationReport
        fields = (
            "student_rr",
            "degree",
            "exemption_request",
            "exemption_report",
            "notes",
        )
        widgets = {
            'student_rr': forms.HiddenInput(),
            'degree': forms.HiddenInput(),
            'notes': forms.HiddenInput(),
        }
