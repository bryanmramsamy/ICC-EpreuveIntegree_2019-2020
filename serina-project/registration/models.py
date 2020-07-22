from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _


class UserProfile(models.Model):
    """Model definition for UserProfile.

    Extension class of the default django.contrib.auth.models.User model.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                verbose_name=_("Username"))
    birthday = models.DateField(auto_now=False, auto_now_add=False,
                                verbose_name=_("Birthday date"))
    nationality = models.CharField(max_length=50,
                                   verbose_name=_("Nationality"))
    address = models.CharField(max_length=255, verbose_name=_("Address"))
    postalCode = models.CharField(max_length=50, verbose_name=_("Postal code"))
    postalLocality = models.CharField(max_length=50,
                                      verbose_name=_("Locality"))

    class Meta:
        """Meta definition for UserProfile."""

        verbose_name = _("User Profile")
        verbose_name_plural = _('User Profiles')

    def __str__(self):
        """Unicode representation of UserProfile."""

        return _("[{}] {}'s profile".format(self.pk, self.user))

    # TODO: Add method when UserProfile url ready
    # def get_absolute_url(self):
    #     """Return absolute url for UserProfile."""
    #     return ('')
