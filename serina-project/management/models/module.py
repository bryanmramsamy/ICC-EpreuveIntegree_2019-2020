from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.shortcuts import reverse
from django.utils.translation import ugettext as _

from .resource import BackOfficeResource


class ModuleLevel(BackOfficeResource):
    """Model definition for ModuleLevel."""

    rank = models.PositiveIntegerField(unique=True, verbose_name=_("Rank"))
    name = models.CharField(max_length=50, verbose_name=_("Name"))

    class Meta:
        """Meta definition for ModuleLevel."""

        verbose_name = _('Module level')
        verbose_name_plural = _('Module levels')
        ordering = ("rank",)

    def __str__(self):
        """Unicode representation of ModuleLevel."""

        return "[{}] (Rank: {}) {}".format(self.pk, self.rank, self.name)

    def clean(self):
        """Clean method for ModuleLevel.

        Check if the creator is a promoted-group's user.
        """

        super().clean()

    def get_absolute_url(self):
        """Return absolute url for ModuleLevel."""

        return reverse('modulelevel_detailview', kwargs={'pk': self.pk})


class Module(BackOfficeResource):
    """Model definition for Module.

    A module is a back-office general representation of a given course.
    A degree is composed of multiple modules.. Only a group of specific
    teachers can teach the module. Some modules cannot be done if the
    prerequisites modules are not finished yet.
    """

    title = models.CharField(
        max_length=255,
        verbose_name=_('Module name'),
        help_text=_("To avoid confusion, it's recommended to use different "
                    "names for each modules.")
    )
    reference = models.CharField(max_length=7, blank=True, unique=True,
                                 verbose_name=_('Reference'))
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Description"),
        help_text=_("Should provide as much information on the module as "
                    "possible."))
    level = models.ForeignKey(
        ModuleLevel,
        null=True,
        on_delete=models.SET_NULL,
        related_name="modules",
        verbose_name=_("Difficulty level"),
        help_text=_("Rank the module by it's diffictuly.")
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
    ECTS_value = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_("ECTS value"),
        help_text=_("Cannot be negative."),
    )
    cost = models.DecimalField(
        null=True,
        max_digits=5,
        decimal_places=2,
        verbose_name=_('Cost per student'),
        help_text=_("Cannot be negative."),
    )
    price = models.DecimalField(
        null=True,
        max_digits=5,
        decimal_places=2,
        verbose_name=_('Student charge price'),
        help_text=_("Cannot be negative."),
    )
    picture = models.ImageField(
        upload_to='management/modules/',
        default='management/books.png',
        null=True,
        blank=True,
        max_length=225,
        verbose_name=_("Picture"),
        help_text=_("Not required. If no picture is sent, the default picture "
                    "will be used.")
    )

    class Meta:
        """Meta definition for Module."""

        verbose_name = _('Module')
        verbose_name_plural = _('Modules')
        ordering = ('title', 'reference')

    @property
    def module_benefits(self):
        """Compute the benefits margin made by one instance of the module."""

        return self.price - self.cost

    @property
    def courses_benefits(self):
        """Compute the benefits margin made by all the module's courses."""

        return self.courses.count() * self.module_benefits

    def __str__(self):
        """Unicode representation of Module."""

        return "[{}] ({}) {}".format(self.pk, self.reference, self.title)

    def clean(self):  # TODO: Fix validators
        """Clean method for Module.

        Check if the creator is a promoted-group's user, if the
        eligible_teachers are from the 'Teacher'-group, if the module has
        not itself has prerequisite and if a postrequisite has been added as
        prerequisite as well.
        """

        # Creator must be a promoted user
        super().clean()

        # TODO: Hide eligible_teachers and prerequisites fields on creation in admin
        # LINK: https://books.agiliq.com/projects/django-admin-cookbook/en/latest/uneditable_existing.html
        if self.pk:
            # eligible_teachers must be "Teacher"-group members
            # TODO: Filter choices in M2M box in admin panel
            for user in self.eligible_teachers.all():
                if not user.groups.filter(name="Teacher").exists():
                    raise ValidationError(
                        _("{} cannot be added as eligible teacher. The user is not"
                        " a 'Teacher'-group member.".format(user.username))
                    )

            # Module can not be its own prerequisite
            # TODO: Does not work on creation, 'pk' empty before save !
            # TODO: Filter choices in M2M box in admin panel
            if self.prerequisites.filter(pk=self.pk).exists():
                raise ValidationError(
                    _("This module can not be its own prerequisite.")
                )

            # prerequisite module cannot be postrequisite too
            # TODO: Does not work on creation, 'pk' empty before save !
            # TODO: Not OK
            # TODO: Filter choices in M2M box in admin panel
            for module in self.prerequisites.all():
                if self.postrequisites.filter(pk=module.pk).exists():
                    raise ValidationError(
                        _("[{0}] {1} cannot be a prerequisite for this module."
                          " [{0}] {1} already has this module as prerequisite."
                          .format(module.reference, module.title))
                    )

    def save(self, *args, **kwargs):
        """Save method for Module.

        Prevent adding eligible_teachers and prerequisites on creation.
        Otherwise, the validations in the clean() won't work (They need
        self.pk which isn't defined yet on creation. These fields can be
        populated on update. Also add a reference based on the module's title
        and pk after generating the pk if it wasn't defined yet.
        """

        self.reference = self.title[0:4].upper()

        if not self.pk:
            super().save(*args, **kwargs)
            self.eligible_teachers.clear()
            self.prerequisites.clear()

        self.reference += str(self.pk).zfill(3)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Return absolute url for Module."""

        return reverse('module_detailview', kwargs={'pk': self.pk})
