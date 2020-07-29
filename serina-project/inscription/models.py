from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.shortcuts import reverse
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

    class Meta:
        """Meta definition for FrontOfficeResource."""

        abstract = True
