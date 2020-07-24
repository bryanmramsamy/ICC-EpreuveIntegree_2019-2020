from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _

from .resource import Resource


class ModuleLevel(Resource):
    """Model definition for ModuleLevel.

    A ranked difficulty level assign to each module.
    """

    rank = models.IntegerField(unique=True, verbose_name=_('Rank'))
    name = models.CharField(max_length=50, verbose_name=_('Name'))

    class Meta:
        """Meta definition for ModuleLevel."""

        verbose_name = 'Modules level'
        verbose_name_plural = 'Modules levels'
        ordering = ('rank', '-date_updated', '-date_created')

    def __str__(self):
        """Unicode representation of ModuleLevel."""

        return "({}) {}".format(self.rank, self.name)

    # TODO: Define method when rooters initialized
    # def get_absolute_url(self):
    #     """Return absolute url for ModuleLevel."""
    #     return ('')


class Module(Resource):
    """Model definition for Module.

    A module is a course.
    This one can be a prerequisite for other modules, which means these
    modules cannot be started as long as this one isn't finisehd yet.
    Each module has can be teached by specific teachers.
    """

    title = models.CharField(max_length=255, verbose_name=_("Title"))
    description = models.TextField(null=True, blank=True,
                                   verbose_name=_("Description"))
    student = models.ManyToManyField(User, related_name='students')
    teachers = models.ManyToManyField(User, related_name='teachers')
    is_prerequisite_for = models.ForeignKey('self', on_delete=models.SET_NULL,
                                            null=True, blank=True,
                                            verbose_name=_(
                                                "Is a prerequisite for"
                                            ))
    level = models.ForeignKey(ModuleLevel, on_delete=models.SET_NULL,
                              null=True, verbose_name=_('Difficulty level'))
    date_start = models.DateField(verbose_name=_('Start date'))
    date_end = models.DateField(verbose_name=_('End date'))
    cost = models.FloatField(verbose_name=_('Cost'))
    fee = models.FloatField(verbose_name=_('Registration fee'))

    class Meta:
        """Meta definition for Module."""

        verbose_name = 'Module'
        verbose_name_plural = 'Modules'

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
