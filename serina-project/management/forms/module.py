from django import forms

from ..models import Module, ModuleLevel
from .resource import BackOfficeResourceFormMixin


class ModuleForm(BackOfficeResourceFormMixin):
    """ModelForm for Module."""

    class Meta(BackOfficeResourceFormMixin.Meta):
        """Meta definition for ModuleLevelForm."""

        model = Module
        exclude = ("reference", "prerequisites", "eligible_teachers")


class ModuleLevelForm(BackOfficeResourceFormMixin):
    """ModelForm for ModuleLevel."""

    class Meta(BackOfficeResourceFormMixin.Meta):
        """Meta definition for ModuleLevelForm."""

        model = ModuleLevel
