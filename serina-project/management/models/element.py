from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _


class ElementMetadata(models.Model):
    """Model definition for ElementMetadata.

    The ElementMetadata contains the creation and update data.
    This abstract model can be inherited by any model in order to avoid adding the same fields on each one.
    """

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                   verbose_name=_('Created by'))
    date_created = models.DateTimeField(auto_now_add=True,
                                        verbose_name=_('Created on'))
    date_updated = models.DateTimeField(auto_now=True,
                                        verbose_name=_('Updated on'))

    class Meta:
        """Meta definition for ElementMetadata."""

        abstract = True
        # verbose_name = "Element's metadata"
        # verbose_name_plural = "Element's metadatas"
