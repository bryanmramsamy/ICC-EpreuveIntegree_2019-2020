from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

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

    module = ModuleChoiceField(
        queryset=Module.objects.all(),
        empty_label=None,
        label=_("Module"),
        help_text=_("Module teached in the created course."),
    )
    teacher = TeacherChoiceField(
        queryset=User.objects.filter(groups__name="Teacher"),
        required=False,
        label=_('Teacher'),
        help_text=_("Teacher of this course."),
    )
    room = ClassroomChoiceField(
        queryset=Classroom.objects.all(),
        required=False,
        label=_('Classroom'),
        help_text=_("Classroom where this course will be given."),
    )

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
