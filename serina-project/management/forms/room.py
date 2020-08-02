from django import forms

from ..models import Classroom
from .resource import BackOfficeResourceFormMixin


# Classroom forms

class ClassroomForm(BackOfficeResourceFormMixin):
    """ModelForm for Classroom."""

    class Meta(BackOfficeResourceFormMixin.Meta):
        """Meta definition for ModuleLevelForm."""

        model = Classroom
