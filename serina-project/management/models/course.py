from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.shortcuts import reverse
from django.utils.translation import ugettext as _

from .module import Module
from .resource import BackOfficeResource
from .room import Classroom


class Course(BackOfficeResource):
    """Model definition for Course."""

    reference = models.CharField(max_length=11, unique=True, blank=True,
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
    picture = models.ImageField(
        upload_to='management/courses/',
        default='management/default.jpg',
        null=True,
        blank=True,
        max_length=225,
        verbose_name=_("Picture"),
    )

    class Meta:
        """Meta definition for Course."""

        verbose_name = _('Course')
        verbose_name_plural = _('Courses')
        ordering = ('date_start', 'reference')

    @property
    def recommended_seats_available(self):
        """Compute the amount of seats left of this course until the
        classroom's recommended capacity is reached."""

        return self.room.recommended_capacity - self.nb_registrants

    @property
    def max_seats_available(self):
        """Compute the amount of seats left of this course until the
        classroom's maximal capacity is reached."""

        return self.room.max_capacity - self.nb_registrants

    @property
    def over_attendance(self):
        """Check if the recommended_capacity has been reached by the expected
        attendance.

        Return None if no room was assigned to the course yet.
        """

        if self.room:
            return self.nb_registrants > self.room.recommended_capacity
        else:
            return None

    def __str__(self):
        """Unicode representation of Course.

        Indictate the teacher's full name if any and the classroom's name if
        any.
        """

        str_result = _("({}) {} course".format(self.reference, self.module.title))

        if self.teacher or self.room:
            str_result += _(" given")

            if self.teacher:
                str_result += _(" by {}".format(self.teacher.get_full_name()))

            if self.room:
                str_result += _(" at {}".format(self.room.name))

        return str_result


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
        # NOTE: Didn't understand why I must use username and not user
        if self.teacher and not self.module.eligible_teachers.filter(
            username=self.teacher.username
        ).exists():
            raise ValidationError(
                _("{} is not eligible to teach this course."
                  .format(self.teacher.get_full_name()))
            )

        # date_start cannot be set after date_end
        if self.date_start and self.date_end \
           and self.date_start >= self.date_end:
            raise ValidationError(
                _("Start date ({}) must be set before end date ({}).".format(
                    self.date_start,
                    self.date_end
                ))
            )

        # nb_registrants must not exceed room.max_capacity
        if self.room and self.nb_registrants > self.room.max_capacity:
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
        self.reference = module_reference + "-"

        if not self.pk:
            super().save(*args, **kwargs)

        self.reference += str(self.pk).zfill(3)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Return absolute url for Course."""

        return reverse('course_detailview', kwargs={'pk': self.pk})
