# TODO: Move this file to a mixin file

from django import forms
from django.utils.translation import ugettext as _


class BackOfficeResourceFormMixin(forms.ModelForm):
    """Mixin for ModelForms thats hide the 'created_by' field and exclude the
    'reference' field if it exist."""

    class Meta:
        """Meta definition for BackOfficeResourceFormMixin."""

        exclude = ("reference",)
        widgets = {
            'created_by': forms.HiddenInput(),
        }


# ModelChoiceFields and ModelMutipleChoiceFields customization

class CategoryLevelChoiceField(forms.ModelChoiceField):
    """Display a formatted name for each DegreeCategory and ModuleLevel in the
    ModelChoiceField."""

    def label_from_instance(self, category_or_level):
        return "{}".format(category_or_level.name)


# TODO: Merge these two classes by finding common inherrited mixin

class ModuleChoiceField(forms.ModelChoiceField):
    """Display the reference and the title of each module in the
    ChoiceField."""

    def label_from_instance(self, module):
        return "{} ({})".format(module.title, module.reference)


class ModuleMultipleChoiceField(forms.ModelMultipleChoiceField):
    """Display the reference and the title of each module in the
    MultipleChoiceField."""

    def label_from_instance(self, module):
        return "{} ({})".format(module.title, module.reference)


# TODO: Merge these two classes by finding common inherrited mixin

class TeacherChoiceField(forms.ModelChoiceField):
    """Display the full name of each teacher in the ChoiceField."""

    def label_from_instance(self, teacher):
        return "{} ({})".format(teacher.get_full_name(), teacher.username)


class TeacherMultipleChoiceField(forms.ModelMultipleChoiceField):
    """Display the full name of each teacher in the MultipleChoiceField."""

    def label_from_instance(self, teacher):
        return "{} ({})".format(teacher.get_full_name(), teacher.username)


class ClassroomChoiceField(forms.ModelChoiceField):
    """Display the full name of each teacher in the ChoiceField."""

    def label_from_instance(self, room):
        return _("{} (Capacity: {}/{})").format(
            room.name,
            room.recommended_capacity,
            room.max_capacity
        )
