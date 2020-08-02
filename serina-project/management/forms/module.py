from django import forms
from django.contrib.auth.models import User
from django.db.models import Q

from ..models import Module, ModuleLevel
from .resource import (
    BackOfficeResourceFormMixin,
    LevelChoiceField,
    ModuleMultipleChoiceField,
    TeacherMultipleChoiceField,
)


# Module forms

class ModuleCreateForm(BackOfficeResourceFormMixin):
    """ModelForm for Module."""

    level = LevelChoiceField(queryset=ModuleLevel.objects.all(), empty_label=None)

    class Meta(BackOfficeResourceFormMixin.Meta):
        """Meta definition for ModuleLevelForm."""

        model = Module
        exclude = ("reference", "prerequisites", "eligible_teachers")


class ModuleUpdateForm(BackOfficeResourceFormMixin):
    """ModelForm for Module.

    Prevent the user to add the instance to its own prerequisites. Also prevent
    adding a postrequisite module to the prerequisites."""

    level = LevelChoiceField(queryset=ModuleLevel.objects.all(), empty_label=None)
    prerequisites = ModuleMultipleChoiceField(queryset=None, required=False)
    eligible_teachers = TeacherMultipleChoiceField(queryset=None,
                                                   required=False)

    def __init__(self, *args, **kwargs):
        """Init of the 'prerequisites'-field queryset."""

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
