from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.shortcuts import reverse
from django.utils.translation import ugettext as _

from .degree_rr import DegreeRegistrationReport
from .resource import FrontOfficeResource
from .student_rr import StudentRegistrationReport

from management.models import Course, Module


class ModuleRegistrationReport(FrontOfficeResource):
    """Model definition for ModuleRegistrationReport.

    Model Registration Report of a model to which the student registered.
    Contains all the related data of the student progression in the module.
    """

    student_rr = models.ForeignKey(
        StudentRegistrationReport,
        on_delete=models.CASCADE,
        related_name="modules_rrs",
        verbose_name=_("Student Registration Report"),
    )
    degree_rr = models.ForeignKey(
        DegreeRegistrationReport,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="modules_rrs",
        verbose_name=_("Degree Registration Report")
    )
    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name="students_registrations",
        verbose_name=_("Registration module")
    )
    course = models.ForeignKey(
        Course,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="students_registrations",
        verbose_name=_("Course")
    )
    date_start = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Start date"),
    )
    date_end = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("End date"),
    )
    student_attempt = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Student's attempt number")
    )  # TODO: Add max_attempt value from settings
    final_score = models.FloatField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name=_("Final score"))
    approved = models.BooleanField(default=False, verbose_name=_("Approved"))
    payed = models.BooleanField(default=False, verbose_name=_("Payed"))

    class Meta:
        """Meta definition for ModuleRegistrationReport."""

        verbose_name = _('Module Registration Report')
        verbose_name_plural = _('Modules Registration Reports')

    @property
    def succeeded(self):
        """Check if the student succeeded the module modules.

        The module succeess is not valid if the student didn't payed his/her
        registration to it.
        """

        return self.approved and self.payed and self.final_score >= 50

    def __str__(self):
        """Unicode representation of ModuleRegistrationReport."""

        return "[{}] {}'s module registration for {}".format(
            self.pk,
            self.student_rr.created_by.get_full_name(),
            self.module.title,
        )

    # TODO: Must be define and redirect to Student Degree's Report template
    # def get_absolute_url(self):
    #     """Return absolute url for DegreeRegistrationRappport."""

    #     return ('')
