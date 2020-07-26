from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _

from .resource import BackOfficeResource


class Classroom(BackOfficeResource):
    """Model definition for Classroom.

    A Classroom is a room which can be assigned to a course and has a
    specific capacity.
    """

    created_by = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        related_name="room_declared_by",
        verbose_name=_('Declared by')
    )
    label = models.CharField(max_length=7, unique=True,
                             verbose_name=_("Label"))
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Description")
    )
    recommended_capacity = models.PositiveIntegerField(
        verbose_name=_("Recommended capacity")
    )
    max_capacity = models.PositiveIntegerField(
        verbose_name=_("Maximum capacity")
    )

    class Meta:
        """Meta definition for Classroom."""

        verbose_name = 'Classroom'
        verbose_name_plural = 'Classrooms'
        ordering = ('label',)

    def __str__(self):
        """Unicode representation of Classroom."""

        return "[{}] {} (Capacity: {}/{})".format(
            self.pk,
            self.label,
            self.recommended_capacity,
            self.max_capacity
        )

    def clean(self):
        # TODO: Comment function
        # TODO: Check if created_by is promoted user
        # NOTE: This function will be used often and must be exported to
        #       separate file to be called
        # TODO: Check if max_capacity is not less than recommended_capacity
        pass

    def save(self, *args, **kwargs):
        """Save method for Classroom.

        Append the Classroom's pk with leading zeros to the label in order to
        make it unique.
        """

        self.label = self.label[0:4].upper()
        super().save(*args, **kwargs)
        self.label += str(self.pk).zfill(3)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Return absolute url for Classroom."""
        return ('')

    # TODO: Define method when rooters are defined
    # def get_absolute_url(self):
    #     """Return absolute url for Classroom."""
    #     return ('')
