from datetime import timedelta

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext as _

from management.models import Degree, Module


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
    date_created = models.DateTimeField(auto_now_add=True,
                                        verbose_name=_("Creation date"))
    date_updated = models.DateTimeField(auto_now=True,
                                        verbose_name=_("Last update date"))
    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="ratings",
        verbose_name=_("Module"),
    )
    degree = models.ForeignKey(
        Degree,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="ratings",
        verbose_name=_("Degree"),
    )
    rate = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name=_("Rate"),
        help_text=_("Give a rate from 1 (very poor) to 5 (very good)"),
    )
    comment = models.TextField(
        max_length=512,
        verbose_name=_("Comment"),
        help_text=_(
            "Leave a comment you want to be displayed on your rate. Your "
            "comment will be shown as well as your rating on the home page "
            "and the module/degree page."
        ),
    )
    is_visible = models.BooleanField(
        default=True,
        verbose_name=_("Is visible"),
    )

    class Meta:
        """Meta definition for StudentRating."""

        verbose_name = 'Rating'
        verbose_name_plural = 'Ratings'
        ordering = ("-date_updated",)

    @property
    def updated_once(self):
        """True if the rating was updated at least once."""

        return self.date_created - self.date_updated > timedelta(0)

    def __str__(self):
        """Unicode representation of StudentRating."""

        if self.module:
            title = self.module.title

        else:
            title = self.degree.title

        return "[{}] {}'s rating on {}".format(
            self.pk,
            self.created_by.get_full_name(),
            title,
        )

    def clean(self):
        """If the rating is related to a module, it cannot be related to a
        degree. The opposite is true as well but it must be related to one of
        them."""

        if not self.module and not self.degree:
            ValidationError(_("A rating must be assigned either to a module "
                              "or to a degree."))

        if self.module and self.degree:
            ValidationError(_("A rating can not be assigned to a module and a "
                              "degree at the same time."))

    def get_absolute_url(self):
        """Return absolute url for StudentRating.

        Redirect to the detail view of the related module or degree.
        """

        if self.module:
            redirection = reverse('module_detailview',
                                  kwargs={'pk': self.module.pk})
        elif self.degree:
            redirection = reverse('degree_detailview',
                                  kwargs={'pk': self.degree.pk})

        return redirection
