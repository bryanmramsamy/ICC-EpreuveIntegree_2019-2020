from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import reverse
from django.utils.translation import ugettext as _

from .module import Module
from .resource import BackOfficeResource


class DegreeCategory(BackOfficeResource):
    """Model definition for DegreeCategory."""

    name = models.CharField(
        max_length=50,
        verbose_name=_("Name"),
        help_text=_("An explicite name is recommended, such as 'Bachelor', "
                    "'PhD', or 'Master'. "),
    )

    class Meta:
        """Meta definition for DegreeCategory."""

        verbose_name = _('Degree category')
        verbose_name_plural = _('Degree categories')
        ordering = ("name",)

    def __str__(self):
        """Unicode representation of DegreeCategory."""

        return "[{}] {}".format(self.pk, self.name)

    def clean(self):
        """Clean method for DegreeCategory.

        Check if the creator is a promoted-group's user.
        """

        super().clean()

    def get_absolute_url(self):
        """Return absolute url for DegreeCategory."""

        return reverse('degreecategory_detailview', kwargs={'pk': self.pk})


class Degree(BackOfficeResource):
    """Model definition for Degree.

    A degree is a back-office general representation of a collection of
    modules leading to a diploma when a student graduate. All the modules from
    the degree must been passed in order to pass the degree itself.
    """

    title = models.CharField(
        max_length=255,
        verbose_name=_("Degree name"),
        help_text=_("To avoid confusion, it's recommended to use different "
                    "names for each degree."),
    )
    reference = models.CharField(max_length=7, unique=True, blank=True,
                                 verbose_name=_('Reference'))
    category = models.ForeignKey(
        DegreeCategory,
        null=True,
        on_delete=models.SET_NULL,
        related_name="degrees",
        verbose_name=_("Degree category")
    )
    modules = models.ManyToManyField(
        Module,
        related_name="degrees",
        verbose_name=_("Modules"),
        help_text=_("All the modules which are part of the degree.")
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Description"),
        help_text=_("Should provide as much information on the module as "
                    "possible.")
    )
    picture = models.ImageField(
        upload_to='management/degrees/',
        default='management/books.png',
        null=True,
        blank=True,
        max_length=225,
        verbose_name=_("Picture"),
        help_text=_("Not required. If no picture is sent, the default picture "
                    "will be used."),
    )

    class Meta:
        """Meta definition for Degree."""

        verbose_name = _('Degree')
        verbose_name_plural = _('Degrees')
        ordering = ('title', 'reference')

    @property
    def nb_modules(self):
        """Get the total of modules being part of the degree."""

        return self.modules.count()

    @property
    def total_ECTS_value(self):
        """Compute the total ECTS value of the degree."""

        total_ects = 0
        for module in self.modules.all():
            total_ects += module.ECTS_value

        return total_ects

    @property
    def total_costs(self):
        """Compute the total costs of the degree."""

        total_costs = 0
        for module in self.modules.all():
            total_costs += module.cost

        return total_costs

    @property
    def total_price(self):
        """Compute the total charges price of the degree."""

        total_costs = 0
        for module in self.modules.all():
            total_costs += module.price

        return total_costs

    @property
    def total_benefits(self):
        """Compute the benefits margin made by one instance of the module."""

        return self.total_price - self.total_costs

    def __str__(self):
        """Unicode representation of Degree."""

        return "[{}] ({}) {}".format(self.pk, self.reference, self.title)

    def clean(self):
        """Clean method for Degree.

        Check if the creator is a promoted-group's user.
        """

        super().clean()

    def save(self, *args, **kwargs):
        """Save method for Degree.

        Add a reference based on the degree's title and pk.
        """

        if not self.pk:
            self.reference = self.title[0:4].upper()

            super().save(*args, **kwargs)

            self.reference += str(self.pk).zfill(3)

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Return absolute url for Degree."""

        return reverse('degree_detailview', kwargs={'pk': self.pk})
