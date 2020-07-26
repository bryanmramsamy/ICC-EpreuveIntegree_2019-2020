from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _

from .module import Module
from .resource import BackOfficeResource


class Classroom(BackOfficeResource):  # TODO: Must be defined in own file
    label = models.CharField(max_length=5)


class Course(BackOfficeResource):
    """Model definition for Course."""

    created_by = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        related_name="course_created_by",
        verbose_name=_('Created by')
    )
    reference = models.CharField(max_length=15, unique=True, blank=True,
                                 verbose_name=_('Reference'))
    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name="courses",
        verbose_name=_("Modules")
    )
    teacher = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        related_name="teached_by",
        verbose_name=_('Teached by')
    )
    room = models.ForeignKey(
        Classroom,  # TODO: Define Classroom class in different file
        null=True,
        on_delete=models.SET_NULL,
        related_name="courses",
        verbose_name=_("Classroom")
    )
    date_start = models.DateField(null=True, blank=True,
                                  verbose_name=_("Start date"))
    date_end = models.DateField(null=True, blank=True,
                                verbose_name=_("End date"))

    class Meta:
        """Meta definition for Course."""

        verbose_name = 'Course'
        verbose_name_plural = 'Courses'
        ordering = ('date_start', 'reference')

    def __str__(self):
        """Unicode representation of Course."""

        return "({}) {} course given by {} at {}".format(
            self.reference,
            self.module.title,
            self.teacher.get_full_name(),
            self.room.label
        )

    def save(self, *args, **kwargs):
        """Save method for Course.

        Add a reference based on the course's pk and it's module name.
        """

        module_reference = self.module.reference
        date_start_reference = self.date_start.strftime("%y%m")
        self.reference = module_reference + '-' + date_start_reference
        super().save(*args, **kwargs)
        self.reference += str(self.pk).zfill(3)
        super().save(*args, **kwargs)

    # TODO: Define method when rooters are defined
    # def get_absolute_url(self):
    #     """Return absolute url for Course."""
    #     return ('')
