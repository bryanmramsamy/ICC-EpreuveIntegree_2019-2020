from django.db import models
from django.utils.translation import ugettext as _

from .module import Module
from .resource import Resource


class CurriculumCategory(Resource):
    """Model definition for CurriculumCategory.

    A category assign to each curriculum.
    """

    name = models.CharField(max_length=50,
                            verbose_name=_('Curriculum category'))

    class Meta:
        """Meta definition for CurriculumCategory."""

        verbose_name = 'Curriculum category'
        verbose_name_plural = 'Curriculum categories'

    def __str__(self):
        """Unicode representation of CurriculumCategory."""

        return "[{}] {}".format(self.pk, self.name)

    # TODO: Define method when rooters initialized
    # def get_absolute_url(self):
    #     """Return absolute url for CurriculumCategory."""
    #     return ('')


class Curriculum(Resource):
    """Model definition for Curriculum.

    A degree or a collection of modules (courses) which, if all it's modules
    has been passed, provides a degree.
    """

    title = models.CharField(max_length=255, verbose_name=_("Title"))
    category = models.OneToOneField(
        CurriculumCategory,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_("Category")
    )
    modules = models.ManyToManyField(Module, related_name='module_curricula',
                                     verbose_name=_('Curricula'))
    description = models.TextField(null=True, blank=True,
                                   verbose_name=_("Description"))

    class Meta:
        """Meta definition for Curriculum."""

        verbose_name = 'Curriculum'
        verbose_name_plural = 'Curricula'
        ordering = ('-date_updated', '-date_created', 'title')

    def __str__(self):
        """Unicode representation of Curriculum."""

        return "[{}] {}: {}".format(self.pk, self.category.name, self.title)

    # TODO: Define method when rooters initialized
    # def get_absolute_url(self):
    #     """Return absolute url for Curriculum."""
    #     return ('')
