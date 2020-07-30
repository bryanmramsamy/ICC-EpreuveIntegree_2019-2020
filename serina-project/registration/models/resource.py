from django.db import models
from django.utils.translation import ugettext as _


class FrontOfficeResource(models.Model):
    """Model definition for FrontOfficeResource.

    A ressource contains a creation and last update timestamp.
    The FrontOfficeResource model is inherited by each front-office model.
    """

    date_created = models.DateTimeField(auto_now_add=True,
                                        verbose_name=_('Created on'))
    date_updated = models.DateTimeField(auto_now=True,
                                        verbose_name=_('Updated on'))
    notes = models.TextField(null=True, blank=True,
                             verbose_name=_("Additional notes"))

    class Meta:
        """Meta definition for FrontOfficeResource."""

        abstract = True
        ordering = ("-date_updated", "-date_created")
