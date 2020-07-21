from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext as _


class UserProfile(models.Model):
    """Model definition for UserProfile.

    Extension class of the default django.contrib.auth.models.User model.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                verbose_name=_("Username"))
    birthday = models.DateField(auto_now=False, auto_now_add=True,
                                verbose_name=_("Birthday date"))
    nationality = models.CharField(default="Unknown", max_length=50,
                                   verbose_name=_("Nationality"))
    address = models.CharField(default="Unknown", max_length=255,
                               verbose_name=_("Address"))
    postalCode = models.CharField(default="Unknown", max_length=50,
                                  verbose_name=_("Postal code"))
    postalLocality = models.CharField(default="Unknown", max_length=50,
                                      verbose_name=_("Locality"))

    class Meta:
        """Meta definition for UserProfile."""

        verbose_name = _("User Profile")
        verbose_name_plural = _('User Profiles')

    def __str__(self):
        """Unicode representation of UserProfile."""

        return _("{}'s profile".format(self.user))

    # TODO: Add method when UserProfile url ready
    # def get_absolute_url(self):
    #     """Return absolute url for UserProfile."""
    #     return ('')


@receiver(post_save, sender=User)
def createUserProfile(sender, instance, created, **kwargs):
    """Create a UserProfile when a User is created and link it to it."""

    if created:
        UserProfile.objects.create(user=instance)
