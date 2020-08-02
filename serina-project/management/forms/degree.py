from django import forms

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

    category = CategoryLevelChoiceField(queryset=DegreeCategory.objects.all(),
                                        empty_label=None)

    class Meta(BackOfficeResourceFormMixin.Meta):
        """Meta definition for DegreeCreateForm."""

        model = Degree
        exclude = ("reference", "modules")


class DegreeUpdateForm(BackOfficeResourceFormMixin):
    """ModelForm for Degree update.

    Prevent the user to add the instance to its own prerequisites. Also prevent
    adding a postrequisite module to the prerequisites."""

    category = CategoryLevelChoiceField(queryset=DegreeCategory.objects.all(),
                                        empty_label=None)
    modules = ModuleMultipleChoiceField(queryset=Module.objects.all(),
                                        required=False)

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
