from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext as _

from ..utilities import member_from_promoted_group_validation
from .resource import BackOfficeResource


class ModuleLevel(BackOfficeResource):
    """Model definition for ModuleLevel."""

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
        """Clean method for ModuleLevel.

        Check if the creator is a promoted-group's user.
        """

        super().clean()

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
    prerequisites = models.ManyToManyField(
        "self",
        blank=True,
        symmetrical=False,
        related_name="postrequisites",
        verbose_name=_("Prerequisites")
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

        return self.courses.count() * self.module_benefits

    def __str__(self):
        """Unicode representation of Module."""

        return "[{}] ({}) {}".format(self.pk, self.reference, self.title)

    def clean(self):  # TODO: Fix validators
        """Clean method for Module.

        Check if the creator is a promoted-group's user, if the
        eligible_teachers are from the 'Professor'-group, if the module has
        not itself has prerequisite and if a postrequisite has been added as
        prerequisite as well.
        """

        # Creator must be a promoted user
        super().clean()

        # eligible_teachers must be "Professor"-group members
        # TODO: Does not work on creation, 'pk' empty before save !
        # for user in self.eligible_teachers.all():
        #     if not user.groups.filter(name="Professor").exists():
        #         raise ValidationError(
        #             _("{} cannot be added as eligible teacher. The user is not"
        #               " a 'Professor'-group member.".format(user.username))
        #         )

        # Module can not be its own prerequisite
        # TODO: Does not work on creation, 'pk' empty before save !
        # if self.prerequisites.filter(pk=self.pk).exists():
        #     raise ValidationError(
        #         _("This module can not be its own prerequisite.")
        #     )

        # prerequisite module cannot be postrequisite too
        # TODO: Does not work on creation, 'pk' empty before save !
        # for module in self.prerequisites.all():
        #     if self.postrequisites.filter(pk=module.pk).exists():
        #         raise ValidationError(
        #             _("[{0}] {1} cannot be a prerequisite for this module. "
        #               "[{0}] {1}  already has this module as prerequisite."
        #               .format(module.reference, module.title))
        #         )

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
