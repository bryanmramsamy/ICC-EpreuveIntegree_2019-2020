from django.core.exceptions import ValidationError
from django.db import models
from django.shortcuts import reverse
from django.utils.translation import ugettext as _

from ..utils import models_utils
from .resource import FrontOfficeResource
from .student_rr import StudentRegistrationReport

from management.models import Degree


class DegreeRegistrationReport(FrontOfficeResource):
    """Model definition for DegreeRegistrationReport.

    Degree Registration Report of a degree to which the student registered.
    Contains all the related data of the student progression in the degree.
    """

    student_registration_report = models.ForeignKey(
        StudentRegistrationReport,
        on_delete=models.CASCADE,
        related_name="degrees_registration_reports",
        verbose_name=_("Student"),)
    degree = models.ForeignKey(
        Degree,
        on_delete=models.CASCADE,
        related_name="students_registrations",
        verbose_name=_("Registration degree")
    )
    date_start = models.DateField(verbose_name=_("Start date"))
    date_end = models.DateField(verbose_name=_("End date"))

    class Meta:
        """Meta definition for DegreeRegistrationReport."""

        verbose_name = _('Degree Registration Report')
        verbose_name_plural = _('Degrees Registration Reports')

    @property
    def academic_years(self):
        """Display the academic years of the sutdent's degree."""

        academic_years = self.date_start.strftime("%Y")

        if self.date_end:
            academic_years += " - {}".format(self.date_end.strftime("%Y"))

        return academic_years

    @property
    def student_graduated(self):
        """Check if the student succeeded all the degree's modules."""

        graduated = True

        for module_registration_report in self.modules_registration_reports\
                .all():
            if not module_registration_report.succeeded:
                graduated = False
                break

        return graduated

    @property
    def average_score(self):
        """Compute the average score of the student."""

        return models_utils.modules_average_score(self)

    @property
    def total_expenses(self):
        """Compute the total expenses of the student for this degree."""

        total_expenses = 0
        for module_registration_report in self.modules_registration_reports\
                                              .all():
            total_expenses += module_registration_report.module.charge_price

        return total_expenses

    def __str__(self):
        """Unicode representation of DegreeRegistrationRappport."""

        return "[{}] {}'s degree registration for {}".format(
            self.pk,
            self.student_registration_report.user.get_full_name(),
            self.degree.title,
        )

    # TODO: Must be define and redirect to Student Degree's Report template
    # def get_absolute_url(self):
    #     """Return absolute url for DegreeRegistrationRappport."""

    #     return ('')
