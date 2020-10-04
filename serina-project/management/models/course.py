from datetime import date, timedelta

from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
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
        verbose_name=_("Module"),
        help_text=_("Module teached in the created course."),
    )
    teacher = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        related_name="teaches",
        verbose_name=_('Teacher'),
        help_text=_("Module teached in the created course."),
    )
    room = models.ForeignKey(
        Classroom,
        null=True,
        on_delete=models.SET_NULL,
        related_name="courses",
        verbose_name=_("Classroom")
    )
    date_start = models.DateField(
        verbose_name=_("Start date"),
        help_text=_("When the course starts."),
    )
    date_end = models.DateField(
        verbose_name=_("End date"),
        help_text=_("When the course ends."),
    )
    prebooked_seats = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Prebooked seats"),
        help_text=_(
            "Seats unbookable by the regular students. Used for V.I.P. and "
            "substracted by the total amount of available seats."
        ),
    )

    class Meta:
        """Meta definition for Course."""

        verbose_name = _('Course')
        verbose_name_plural = _('Courses')
        ordering = ('date_start', 'reference')

    @property
    def nb_registrants(self):
        """Compute the total of registrants of this course.

        The amount is the sum of the prebooked seats and the total amount of
        accepted, payed or completed module registration requests for this
        course.
        """

        return self.prebooked_seats + course_nb_registrants(self)

    @property
    def recommended_seats_available(self):
        """Compute the amount of seats left of this course until the
        classroom's recommended capacity is reached."""

        return self.room.recommended_capacity - self.nb_registrants

    @property
    def recommended_attendance_percentage(self):
        """Compute the percentage of attendance compared to the total
        recommended capacity amount."""

        return (self.nb_registrants/self.room.recommended_capacity)

    @property
    def max_seats_available(self):
        """Compute the amount of seats left of this course until the
        classroom's maximal capacity is reached."""

        return self.room.max_capacity - self.nb_registrants

    @property
    def max_attendance_percentage(self):
        """Compute the percentage of attendance compared to the total maximum
        capacity amount."""

        return (self.nb_registrants/self.room.max_capacity)

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

    @property
    def status(self):
        """Check the status of the course based on its 'date_start' and
        'date_end' attributes.

        The 'UPCOMING'-status indicates the course hasn't started yet.
        The 'ONGOING'-status indicates the course has already started but is
        not finished yet.
        The 'FINISHED'-status indicates that the course is already finished.
        """

        today = date.today()

        if self.date_start < today and today < self.date_end:
            status = 'ONGOING'
        elif self.date_end < today:
            status = 'FINISHED'
        else:
            status = 'UPCOMING'

        return status

    @property
    def still_registrable(self):
        """Check if it is not too late to be assigned to this course.

        The maximum amount of days of attendance per course required is defined
        by the settings.COURSE_MINIMUM_REGISTRATION_DAYS value.
        """

        return (self.date_end - date.today()) >= timedelta(
            days=settings.COURSE_MINIMUM_REGISTRATION_DAYS,
        )

    def __str__(self):
        """Unicode representation of Course.

        Indictate the teacher's full name if any and the classroom's name if
        any.
        """

        str_result = _("({}) {} course".format(self.reference,
                                               self.module.title))

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

        # date_start cannot be set in the past
        if self.date_start < date.today():
            raise ValidationError(
                _("Start date ({}) must be set after today's date ({})."
                    .format(self.date_start, date.today()))
                )

        # nb_registrants must not exceed room.max_capacity
        if self.room and self.nb_registrants > self.room.max_capacity:
            raise ValidationError(
                _("Amount of registrants ({}) cannot be higher than the "
                  "maximum capacity of the assigned classroom ({}).".format(
                    self.nb_registrants,
                    self.room.max_capacity,
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


def course_nb_registrants(course):
    """Count the amount of module registration request for the given course."""

    # Local import to avoid circular import issue
    from registration.models import ModuleRegistrationReport

    return ModuleRegistrationReport.objects.filter(
        Q(course=course),
        Q(Q(status="APPROVED") | Q(status="PAYED") | Q(status="COMPLETED")),
    ).count()
