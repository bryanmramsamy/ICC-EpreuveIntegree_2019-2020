from django import forms
from django.db.models import Q

from ..models import Module, ModuleLevel
from .resource import BackOfficeResourceFormMixin


class ModuleCreateForm(BackOfficeResourceFormMixin):
    """ModelForm for Module."""

    class Meta(BackOfficeResourceFormMixin.Meta):
        """Meta definition for ModuleLevelForm."""

        model = Module
        exclude = ("reference", "prerequisites", "eligible_teachers")

class MyModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return "{}".format(obj.title)

class ModuleUpdateForm(BackOfficeResourceFormMixin):
    """ModelForm for Module.

    Prevent the user to add the instance to its own prerequisites. Also prevent
    adding a postrequisite module to the prerequisites."""

    prerequisites = MyModelMultipleChoiceField(queryset=None)

    def __init__(self, *args, **kwargs):
        """Init of the 'prerequisites'-field queryset."""

        super().__init__(*args, **kwargs)
        self.fields['prerequisites'].queryset = Module.objects.exclude(
            pk=self.instance.pk).exclude(prerequisites=self.instance)

    class Meta(BackOfficeResourceFormMixin.Meta):
        """Meta definition for ModuleLevelForm."""

        model = Module
        exclude = ("reference",)


class ModuleLevelForm(BackOfficeResourceFormMixin):
    """ModelForm for ModuleLevel."""

    class Meta(BackOfficeResourceFormMixin.Meta):
        """Meta definition for ModuleLevelForm."""

        model = ModuleLevel
