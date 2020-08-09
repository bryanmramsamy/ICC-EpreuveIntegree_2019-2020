from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import ugettext as _

from management.models import Module


class StudentRating(models.Model):
    """Model definition for StudentRating.

    A StudentRating is a rate left by a student that succeeded a module.
    This is in order to give a feed-back to the teachers and improve  how the
    module is been teached and evaluated.
    """

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="ratings",
        verbose_name=_("Student"),
    )
    date_created = models.DateField(auto_now_add=True,
                                    verbose_name=_("Creation date"))
    date_updated = models.DateField(auto_now=True,
                                    verbose_name=_("Creation date"))
    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name="ratings",
        verbose_name=_("Module"),
    )
    rate = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name=_("Rate"),
    )
    comment = models.TextField(verbose_name=_("Comment"))

    class Meta:
        """Meta definition for StudentRating."""

        verbose_name = 'Rating'
        verbose_name_plural = 'Ratings'
        ordering = ("-date_updated",)

    def __str__(self):
        """Unicode representation of StudentRating."""

        return "[{}] {}'s rating on {}".format(
            self.pk,
            self.user.get_full_name(),
            self.module.title,
        )

    # def save(self):
    #     """Save method for StudentRating."""

        # TODO: Prevent student from leaving multiple rates on the same module

    # TODO: Must be define and redirect to Student Degree's Report template
    # def get_absolute_url(self):
    #     """Return absolute url for DegreeRegistrationRappport."""

    #     return ('')
