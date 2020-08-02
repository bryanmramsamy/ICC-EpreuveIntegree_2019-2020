from django import forms

from ..models import Degree, DegreeCategory
from .resource import (
    BackOfficeResourceFormMixin,
    ModuleMultipleChoiceField,
    TeacherMultipleChoiceField,
)

# Degree forms

class DegreeCreateForm(BackOfficeResourceFormMixin):
    """ModelForm for Module."""

    class Meta(BackOfficeResourceFormMixin.Meta):
        """Meta definition for ModuleLevelForm."""

        model = Degree
        exclude = ("reference", "modules")


# class ModuleUpdateForm(BackOfficeResourceFormMixin):
#     """ModelForm for Module.

#     Prevent the user to add the instance to its own prerequisites. Also prevent
#     adding a postrequisite module to the prerequisites."""

#     level = LevelChoiceField(queryset=ModuleLevel.objects.all(), empty_label=None)
#     prerequisites = ModuleMultipleChoiceField(queryset=None, required=False)
#     eligible_teachers = TeacherMultipleChoiceField(queryset=None,
#                                                    required=False)

#     def __init__(self, *args, **kwargs):
#         """Init of the 'prerequisites'-field queryset."""

#         super().__init__(*args, **kwargs)
#         self.fields['prerequisites'].queryset = \
#             Module.objects.exclude(pk=self.instance.pk) \
#                           .exclude(prerequisites=self.instance)

#         self.fields['eligible_teachers'].queryset = \
#             User.objects.filter(groups__name="Teacher")

#     class Meta(BackOfficeResourceFormMixin.Meta):
#         """Meta definition for ModuleLevelForm."""

#         model = Module
#         exclude = ("reference",)


# ModuleLevel forms

class DegreeCategoryForm(BackOfficeResourceFormMixin):
    """ModelForm for DegreeCategory."""

    class Meta(BackOfficeResourceFormMixin.Meta):
        """Meta definition for ModuleLevelForm."""

        model = DegreeCategory
