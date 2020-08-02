from django import forms


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

class LevelChoiceField(forms.ModelChoiceField):
    """Display a formatted name for each ModuleLevel in the
    ModelChoiceField."""

    def label_from_instance(self, level):
        return "{}".format(level.name)


class ModuleMultipleChoiceField(forms.ModelMultipleChoiceField):
    """Display the reference and the title of each module in the
    MultipleChoiceField."""

    def label_from_instance(self, module):
        return "{} ({})".format(module.title, module.reference)


class TeacherMultipleChoiceField(forms.ModelMultipleChoiceField):
    """Display the full name of each teacher in the MultipleChoiceField."""

    def label_from_instance(self, teacher):
        return "{} ({})".format(teacher.get_full_name(), teacher.username)