from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _

from .resource import BackOfficeResource


class ModuleLevel(BackOfficeResource):
    """Model definition for ModuleLevel."""

    created_by = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        related_name="created_module_levels",
        verbose_name=_('Created by')
    )
    rank = models.PositiveIntegerField(unique=True, verbose_name=_("Rank"))
    name = models.CharField(max_length=50, verbose_name=_("Name"))

    class Meta:
        """Meta definition for ModuleLevel."""

        verbose_name = 'Module level'
        verbose_name_plural = 'Module levels'
        ordering = ("rank",)

    def __str__(self):
        """Unicode representation of ModuleLevel."""

        return "[{}] (Rank: {}) {}".format(self.pk, self.rank, self.name)

    def clean(self):
        # TODO: Comment function
        # TODO: Check if created_by is promoted user
        # NOTE: This function will be used often and must be exported to
        #       separate file to be called
        pass

    # TODO: Define method when rooters are defined
    # def get_absolute_url(self):
    #     """Return absolute url for ModuleLevel."""
    #     return ('')


class Module(BackOfficeResource):
    """Model definition for Module.

    A module is a back-office general representation of a given course.
    A degree is composed of multiple modules.. Only a group of specific
    teachers can teach the module. Some modules cannot be done if the
    prerequisites modules are not finished yet.
    """

    created_by = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        related_name="created_modules",
        verbose_name=_('Created by'))
    title = models.CharField(max_length=255, verbose_name=_('Module'))
    reference = models.CharField(max_length=7, blank=True, unique=True,
                                 verbose_name=_('Reference'))
    description = models.TextField(null=True, blank=True,
                                   verbose_name=_("Description"))
    level = models.ForeignKey(
        ModuleLevel,
        null=True,
        on_delete=models.SET_NULL,
        related_name="modules",
        verbose_name=_("Difficultiy level")
    )
    prerequisite = models.ManyToManyField(
        "self",
        blank=True,
        related_name="postrequisites",
        verbose_name=_("Is a prerequisite for (Modules)")
    )
    eligible_teachers = models.ManyToManyField(
        User,
        blank=True,
        related_name="teachable_modules",
        verbose_name=_("Eligible teachers")
    )
    ECTS_value = models.PositiveIntegerField(null=True, blank=True,
                                             verbose_name=_("ECTS value"))
    cost = models.FloatField(null=True, verbose_name=_('Cost'))
    charge_price = models.FloatField(null=True,
                                     verbose_name=_('Charge price'))

    class Meta:
        """Meta definition for Module."""

        verbose_name = 'Module'
        verbose_name_plural = 'Modules'
        ordering = ('title', 'reference')

    @property
    def module_benefits(self):
        """Compute the benefits margin made by one instance of the module"""

        return self.charge_price - self.cost

    @property
    def courses_benefits(self):
        """Compute the benefits margin made by all the module's courses"""

        # TODO: Course model must be defined (related_name="courses")
        return self.courses.count() * self.module_benefits

    def __str__(self):
        """Unicode representation of Module."""

        return "[{}] ({}) {}".format(self.pk, self.reference, self.title)

    def clean(self):
        # TODO: Comment function
        # TODO: Check if created_by is promoted user
        # NOTE: This function will be used often and must be exported to
        #       separate file to be called
        # TODO: Check if eligible_teachers's Users are from "Professor"-group
        pass

    def save(self, *args, **kwargs):
        """Save method for Module.

        Add a reference based on the module's title and pk.
        """

        self.reference = self.title[0:4].upper()
        super().save(*args, **kwargs)
        self.reference += str(self.pk).zfill(3)
        super().save(*args, **kwargs)

    # TODO: Define method when rooters are defined
    # def get_absolute_url(self):
    #     """Return absolute url for Module."""
    #     return ('')
