from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _


class Resource(models.Model):
    """Model definition for Resource.

    The Resource contains the creation and update data.
    This abstract model can be inherited by any model in order to avoid adding
    the same fields on each one.
    """

    created_by = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        related_name="created_by",
        # TODO: Remove note after adding it to notes file
        # NOTE: Instead of resource.created_by_set.all(), use resource.created_by.all()
        # FOO_set is the default fieldname given by the Manager
        # https://docs.djangoproject.com/en/3.0/topics/db/queries/#following-relationships-backward
        verbose_name=_('Created by'))
    date_created = models.DateTimeField(auto_now_add=True,
                                        verbose_name=_('Created on'))
    date_updated = models.DateTimeField(auto_now=True,
                                        verbose_name=_('Updated on'))

    class Meta:
        """Meta definition for Resource."""

        abstract = True
        ordering = ('-date_updated', '-date_created')
