from django import forms
from django.utils.translation import gettext_lazy as _

from ..models import Degree, DegreeCategory, Module
from .resource import (
    BackOfficeResourceFormMixin,
    CategoryLevelChoiceField,
    ModuleMultipleChoiceField,
    TeacherMultipleChoiceField,
)


# Degree forms

class DegreeCreateForm(BackOfficeResourceFormMixin):
    """ModelForm for Degree creation."""

    category = CategoryLevelChoiceField(
        queryset=DegreeCategory.objects.all(),
        empty_label=None,
        label=_("Degree category"),
        help_text=_("Defines the academic level of the degree."),
    )

    class Meta(BackOfficeResourceFormMixin.Meta):
        """Meta definition for DegreeCreateForm."""

        model = Degree
        exclude = ("reference", "modules")


class DegreeUpdateForm(BackOfficeResourceFormMixin):
    """ModelForm for Degree update.

    Prevent the user to add the instance to its own prerequisites. Also prevent
    adding a postrequisite module to the prerequisites."""

    category = CategoryLevelChoiceField(
        queryset=DegreeCategory.objects.all(),
        empty_label=None,
        label=_("Degree category"),
        help_text=_("Defines the academic level of the degree."),
    )
    modules = ModuleMultipleChoiceField(
        queryset=Module.objects.all(),
        required=False,
        label=_("Modules"),
        help_text=_("All the modules which are part of the degree.")
    )

    class Meta(BackOfficeResourceFormMixin.Meta):
        """Meta definition for ModuleLevelForm."""

        model = Degree
        exclude = ("reference",)


# DegreeCategory forms

class DegreeCategoryForm(BackOfficeResourceFormMixin):
    """ModelForm for DegreeCategory."""

    class Meta(BackOfficeResourceFormMixin.Meta):
        """Meta definition for ModuleLevelForm."""

        model = DegreeCategory
