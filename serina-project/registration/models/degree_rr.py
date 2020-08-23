from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.shortcuts import reverse
from django.utils.translation import ugettext as _

from . import resource
from .student_rr import StudentRegistrationReport

from management.models import Degree


class DegreeRegistrationReport(resource.FrontOfficeResource):
    """Model definition for DegreeRegistrationReport.

    Degree Registration Report of a degree to which the student registered.
    Contains all the related data of the student progression in the degree.
    """

    student_rr = models.ForeignKey(
        StudentRegistrationReport,
        on_delete=models.CASCADE,
        related_name="degrees_rrs",
        verbose_name=_("Student"),
    )
    degree = models.ForeignKey(
        Degree,
        on_delete=models.CASCADE,
        related_name="students_registrations",
        verbose_name=_("Registration degree")
    )
    date_payed = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Payment date"),
    )

    class Meta:
        """Meta definition for DegreeRegistrationReport."""

        verbose_name = _('Degree Registration Report')
        verbose_name_plural = _('Degrees Registration Reports')

    @property
    def partially_approved(self):
        """Check if at least one of the related modules_rr is approved.

        Return 'None' if  there is no modules_rrs in the degree_rr.
        """

        partially_approved = None

        for module_rr in self.modules_rrs.all():
            partially_approved = False

            if module_rr.approved:
                partially_approved = True
                break

        return partially_approved

    @property
    def fully_approved(self):
        """Check if all the related modules_rr are approved.

        Return 'None' if  there is no modules_rrs in the degree_rr.
        """

        fully_approved = None

        for module_rr in self.modules_rrs.all():
            fully_approved = True

            if not module_rr.approved:
                fully_approved = False
                break

        return fully_approved

    @property
    def partially_payed(self):
        """Check if at least one of the related modules_rr is approved.

        Return 'None' if  there is no modules_rrs in the degree_rr.
        """

        partially_payed = None

        for module_rr in self.modules_rrs.all():
            partially_payed = False

            if module_rr.payed:
                partially_payed = True
                break

        return partially_payed

    @property
    def fully_payed(self):
        """Check if all the related modules_rr are payed.

        Return 'None' if  there is no modules_rrs in the degree_rr.
        """

        fully_payed = None

        for module_rr in self.modules_rrs.all():
            fully_payed = True

            if not module_rr.payed:
                fully_payed = False
                break

        return fully_payed

    @property
    def student_graduated(self):
        """Check if the student succeeded all the degree's modules."""

        student_graduated = True

        for module_rr in self.modules_rrs.all():
            if not (module_rr.status == 'COMPLETED'
                    or module_rr.status == 'EXEMPTED'):
                student_graduated = False
                break

        return student_graduated

    @property
    def average_score(self):
        """Compute the average score of the student."""

        return resource.modules_average_score(self)

    @property
    def total_paid_price(self):
        """Compute the total price of the student for this degree.

        The denied and exempted modules are not included into the price.
        """

        total_paid_price = 0
        for module_rr in self.modules_rrs.filter(
            Q(status='APPROVED')
            | Q(status='PAYED')
            | Q(status='COMPLETED')
        ):
            total_paid_price += module_rr.module.price

        return total_paid_price

    def __str__(self):
        """Unicode representation of DegreeRegistrationRappport."""

        return "[{}] {}'s degree registration for {}".format(
            self.pk,
            self.student_rr.created_by.get_full_name(),
            self.degree.title,
        )

    def get_absolute_url(self):
        """Return absolute url for DegreeRegistrationRappport."""

        return reverse("degree_rr_detailview", kwargs={"pk": self.pk})
