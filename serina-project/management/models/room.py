from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.shortcuts import reverse
from django.utils.translation import ugettext as _

from .resource import BackOfficeResource


class Classroom(BackOfficeResource):
    """Model definition for Classroom.

    A Classroom is a room which can be assigned to a course and has a
    specific capacity.
    """

    name = models.CharField(
        max_length=50,
        verbose_name=_("Designation"),
        help_text=_("Must be as short and descriptive as possible."),
    )
    reference = models.CharField(max_length=7, blank=True, unique=True,
                                 verbose_name=_('Reference'))
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Description"),
        help_text=_("Should provide as much information on the module as "
                    "possible.")
    )
    recommended_capacity = models.PositiveIntegerField(
        verbose_name=_("Recommended capacity"),
        help_text=_("Capacity where the attendees can work in optimal "
                    "conditions."),
    )
    max_capacity = models.PositiveIntegerField(
        verbose_name=_("Maximum capacity"),
        help_text=_("Maximal capacity in case of over attendance."),
    )
    picture = models.ImageField(
        upload_to='management/rooms/',
        default='management/books.png',
        null=True,
        blank=True,
        max_length=225,
        verbose_name=_("Picture"),
        help_text=_("Not required. If no picture is sent, the default picture "
                    "will be used."),
    )

    class Meta:
        """Meta definition for Classroom."""

        verbose_name = _('Classroom')
        verbose_name_plural = _('Classrooms')
        ordering = ('name', 'reference')

    def __str__(self):
        """Unicode representation of Classroom."""

        return "({}) {} (Capacity: {}/{})".format(
            self.reference,
            self.name,
            self.recommended_capacity,
            self.max_capacity
        )

    def clean(self):
        """Clean method for Classroom.

        Check if the creator is a promoted-group's user.
        """

        # Creator must be a promoted user
        super().clean()

        # recommended_capacity cannot be
        if self.recommended_capacity == 0 or self.max_capacity == 0:
            raise ValidationError(
                _("The capacity of a classroom cannot be zero.")
            )

        # recommended_capacity cannot be higher than max_capacity
        if self.recommended_capacity > self.max_capacity:
            raise ValidationError(
                _("The recommended capacity ({}) cannot be higher than the "
                  "maximum capacity ({}).".format(self.recommended_capacity,
                                                  self.max_capacity))
            )

    def save(self, *args, **kwargs):
        """Save method for Classroom.

        Append the Classroom's pk with leading zeros to the label in order to
        make it unique.
        """


        if not self.pk:
            self.reference = self.name[0:4].upper()

            super().save(*args, **kwargs)

            self.reference += str(self.pk).zfill(3)

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Return absolute url for Classroom."""

        return reverse('classroom_detailview', kwargs={'pk': self.pk})
