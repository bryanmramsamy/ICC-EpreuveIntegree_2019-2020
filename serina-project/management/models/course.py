from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext as _

from ..utilities import member_from_promoted_group_validation
from .module import Module
from .resource import BackOfficeResource
from .room import Classroom


class Course(BackOfficeResource):
    """Model definition for Course."""

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
        related_name="teaches",
        verbose_name=_('Teached by')
    )
    room = models.ForeignKey(
        Classroom,
        null=True,
        on_delete=models.SET_NULL,
        related_name="courses",
        verbose_name=_("Classroom")
    )
    date_start = models.DateField(null=True, blank=True,
                                  verbose_name=_("Start date"))
    date_end = models.DateField(null=True, blank=True,
                                verbose_name=_("End date"))
    nb_registrants = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Amount of registrants")
    )

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

    def clean(self):
        """Clean method for Course.

        Check if the creation date is not set after the last update date, if
        the creator of the instance is a user from a promoted group
        ('Professor', 'Manager' or 'Administrator'), if the teacher is
        eligible to teach this module, if the start date is set before the end
        date and if the amount of registrants is not higher than the maximum
        capacity of the assigned classroom.

        Check if the creator is a promoted-group's user.
        """

        # Creator must be a promoted user
        super().clean()

        # Teacher must be eligilble for module
        # TODO: Not tested yet
        if not self.module.eligible_teachers.filter(
            # NOTE: Didn't understand why I must use username and not user
            username=self.teacher.username
        ).exists():
            raise ValidationError(
                _("{} is not eligible to teach this course."
                  .format(self.teacher.get_full_name()))
            )

        # date_start cannot be set after date_end
        # TODO: Not tested yet
        if self.date_start >= self.date_end:
            raise ValidationError(
                _("Start date ({}) must be set before end date ({}).".format(
                    self.date_start,
                    self.date_end
                ))
            )

        # nb_registrants must not exceed room.max_capacity
        # TODO: Not tested yet
        if self.nb_registrants > self.room.max_capacity:
            raise ValidationError(
                _("Amount of registrants ({}) cannot be higher than the "
                  "maximum capacity of the assigned classroom ({}).".format(
                      self.nb_registrants,
                      self.room.max_capacity
                  ))
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
