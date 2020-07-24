from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _

from .element import Element


class Module(Element):
    """Model definition for Module."""

    title = models.CharField(max_length=255, verbose_name=_("Title"))
    description = models.TextField(null=True, blank=True,
                                   verbose_name=_("Description"))
    is_prerequisite_for = models.ForeignKey('self', on_delete=models.SET_NULL,
                                            null=True, blank=True,
                                            verbose_name=_(
                                                "Is a prerequisite for"
                                            ))
    # level = models.ForeignKey(ModuleLevel, on_delete=models.SET_NULL,
    #                           null=True, verbose_name=_('Difficulty level'))
    # TODO: Define ModuleLevel model first
    cost = models.FloatField(verbose_name=_('Cost'))
    fee = models.FloatField(verbose_name=_('Registration fee'))
    nbPeriods = models.PositiveIntegerField(verbose_name=_('Periods'))

    class Meta:
        """Meta definition for Module."""

        verbose_name = 'Module'
        verbose_name_plural = 'Modules'
        ordering = ('-date_created',)

    def __str__(self):
        """Unicode representation of Module."""

        return "[{}] {}".format(self.pk, self.title)

    # TODO: Check if save must be overriden
    # def save(self):
    #     """Save method for Module."""
    #     pass

    # TODO: Define method when rooters initialized
    # def get_absolute_url(self):
    #     """Return absolute url for Module."""
    #     return ('')
