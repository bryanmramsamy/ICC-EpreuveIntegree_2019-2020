from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext as _

from registration.utilities.groups_utils import is_back_office_user


class BackOfficeResource(models.Model):
    """Model definition for BackOfficeResource.

    A ressource contains a creation and last update timestamp.
    The BackOfficeResource model is inherited by each back-office model.
    """

    created_by = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        related_name="created_%(class)s",
        verbose_name=_('Created by')
    )
    date_created = models.DateTimeField(auto_now_add=True,
                                        verbose_name=_('Created on'))
    date_updated = models.DateTimeField(auto_now=True,
                                        verbose_name=_('Updated on'))

    class Meta:
        """Meta definition for BackOfficeResource."""

        abstract = True

    def clean(self):
        """Check if a the created_by user is part of a promoted group and
        raise an error otherwise.

        The promoted groups are 'Professor', 'Manager' and 'Administrator'.
        """

        if not is_back_office_user(self.created_by):
            raise ValidationError(
                _("{} is not allowed to perform back-office tasks like this. "
                  "These action must be performed by a promoted user."
                  .format(self.created_by.username))
            )
