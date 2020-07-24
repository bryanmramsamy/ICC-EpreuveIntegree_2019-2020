from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _


class Resource(models.Model):
    """Model definition for Resource.

    The Resource contains the creation and update data.
    This abstract model can be inherited by any model in order to avoid adding
    the same fields on each one.
    """

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                   verbose_name=_('Created by'))
    date_created = models.DateTimeField(auto_now_add=True,
                                        verbose_name=_('Created on'))
    date_updated = models.DateTimeField(auto_now=True,
                                        verbose_name=_('Updated on'))

    class Meta:
        """Meta definition for Resource."""

        abstract = True
        # verbose_name = "Resource's metadata"
        # verbose_name_plural = "Resource's metadatas"
        ordering = ('-date_updated', '-date_created')