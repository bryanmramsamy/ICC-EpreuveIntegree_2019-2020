from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext as _


class BackOfficeResource(models.Model):
    """Model definition for BackOfficeResource.

    A ressource contains a creation and last update timestamp.
    The BackOfficeResource model is inherited by each back-office model.
    """

    date_created = models.DateTimeField(auto_now_add=True,
                                        verbose_name=_('Created on'))
    date_updated = models.DateTimeField(auto_now=True,
                                        verbose_name=_('Updated on'))

    class Meta:
        """Meta definition for BackOfficeResource."""

        abstract = True

    def clean(self):
        """Check if the created date is not set after the updated date."""

        if self.date_created > self.date_updated:
            raise ValidationError(
                _("Last update date ({}) cannot be set before created "
                  " date({}).".format(self.date_updated, self.date_created))
            )
