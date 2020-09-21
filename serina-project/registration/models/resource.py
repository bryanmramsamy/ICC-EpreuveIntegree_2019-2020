from django.db import models
from django.utils.translation import ugettext as _


class FrontOfficeResource(models.Model):
    """Model definition for FrontOfficeResource.

    A ressource contains a creation and last update timestamp.
    The FrontOfficeResource model is inherited by each front-office model.
    """

    date_created = models.DateTimeField(auto_now_add=True,
                                        verbose_name=_('Created on'))
    date_updated = models.DateTimeField(auto_now=True,
                                        verbose_name=_('Updated on'))
    notes = models.TextField(null=True, blank=True,
                             verbose_name=_("Additional notes"))

    class Meta:
        """Meta definition for FrontOfficeResource."""

        abstract = True
        ordering = ("-date_updated", "-date_created")


def modules_average_score(student_or_degree_rr):
    """Compute the average score the student got for each of his/her finished
    module.

    If the student didn't followed a single module, the result will be -1.
    """

    sum_score = 0
    total_module = student_or_degree_rr.modules_rrs \
                                       .filter(final_score__isnull=False) \
                                       .count()

    if total_module > 0:
        for module_student_or_degree_rr in student_or_degree_rr.modules_rrs \
                                           .filter(final_score__isnull=False):
            sum_score += module_student_or_degree_rr.final_score

        return round(sum_score / total_module, 2)
    else:
        return -1
