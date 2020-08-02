from django import forms
from django.contrib.auth.models import User

from ..models import Classroom, Course, Module
from .resource import (
    BackOfficeResourceFormMixin,
    ClassroomChoiceField,
    ModuleChoiceField,
    TeacherChoiceField,
)


# Course forms

class CourseCreateForm(BackOfficeResourceFormMixin):
    """ModelForm for Course."""

    module = ModuleChoiceField(queryset=Module.objects.all(), empty_label=None)
    teacher = TeacherChoiceField(queryset=None, required=False)
    room = ClassroomChoiceField(queryset=Classroom.objects.all(),
                                required=False)

    def __init__(self, *args, **kwargs):
        """Init of the 'prerequisites' and the 'eligible_teacher'-fields
        queryset."""

        super().__init__(*args, **kwargs)
        self.fields['teacher'].queryset = \
            User.objects.filter(groups__name="Teacher")

    class Meta(BackOfficeResourceFormMixin.Meta):
        """Meta definition for ModuleLevelForm."""

        model = Course


class CourseUpdateForm(CourseCreateForm):
    """UpdateForm for Course."""

    def __init__(self, *args, **kwargs):
        """Init of the 'prerequisites' and the 'eligible_teacher'-fields
        queryset."""

        super().__init__(*args, **kwargs)
        self.fields['teacher'].queryset = \
            User.objects.filter(groups__name="Teacher") \
                .filter(teachable_modules=self.instance.module)
