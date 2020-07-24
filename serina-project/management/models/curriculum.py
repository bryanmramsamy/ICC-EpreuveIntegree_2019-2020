from django.db import models
from django.utils.translation import ugettext as _

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

    # # TODO: Define method when rooters initialized
    # def get_absolute_url(self):
    #     """Return absolute url for CurriculumCategory."""
    #     return ('')
