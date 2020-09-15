from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from ..models import Module, ModuleLevel
from .resource import (
    BackOfficeResourceFormMixin,
    CategoryLevelChoiceField,
    ModuleMultipleChoiceField,
    TeacherMultipleChoiceField,
)


# Module forms

class ModuleCreateForm(BackOfficeResourceFormMixin):
    """ModelForm for Module."""

    level = CategoryLevelChoiceField(
        queryset=ModuleLevel.objects.all(),
        empty_label=None,
        label=_("Difficulty level"),
        help_text=_("Rank the module by it's diffictuly."),
    )

    class Meta(BackOfficeResourceFormMixin.Meta):
        """Meta definition for ModuleLevelForm."""

        model = Module
        exclude = ("reference", "prerequisites", "eligible_teachers")


class ModuleUpdateForm(BackOfficeResourceFormMixin):
    """ModelForm for Module.

    Prevent the user to add the instance to its own prerequisites. Also prevent
    adding a postrequisite module to the prerequisites."""

    level = CategoryLevelChoiceField(
        queryset=ModuleLevel.objects.all(),
        empty_label=None,
        label=_("Difficulty level"),
        help_text=_("Rank the module by it's diffictuly."),
    )
    prerequisites = ModuleMultipleChoiceField(
        queryset=None,
        required=False,
        label=_("Prerequisites"),
        help_text=_("Select the prerequisite modules."),
    )
    eligible_teachers = TeacherMultipleChoiceField(
        queryset=None,
        required=False,
        label=_("Eligible teachers"),
        help_text=_("Select the teachers whom are able to teach this module."),
    )

    def __init__(self, *args, **kwargs):
        """Init of the 'prerequisites' and the 'eligible_teacher'-fields
        queryset."""

        super().__init__(*args, **kwargs)
        self.fields['prerequisites'].queryset = \
            Module.objects.exclude(pk=self.instance.pk) \
                          .exclude(prerequisites=self.instance)

        self.fields['eligible_teachers'].queryset = \
            User.objects.filter(groups__name="Teacher")

    class Meta(BackOfficeResourceFormMixin.Meta):
        """Meta definition for ModuleLevelForm."""

        model = Module
        exclude = ("reference",)


# ModuleLevel forms

class ModuleLevelForm(BackOfficeResourceFormMixin):
    """ModelForm for ModuleLevel."""

    class Meta(BackOfficeResourceFormMixin.Meta):
        """Meta definition for ModuleLevelForm."""

        model = ModuleLevel
