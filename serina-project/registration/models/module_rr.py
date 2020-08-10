from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
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
        related_name="modules_rrs",
        verbose_name=_("Registration module")
    )
    course = models.ForeignKey(
        Course,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="modules_rrs",
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
    date_payed = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Payment date"),
    )
    nb_attempt = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Student's attempt number")
    )  # TODO: Add max_attempt value from settings
    final_score = models.DecimalField(
        null=True,
        blank=True,
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name=_("Final score")
    )

    MODULE_REGISTRATION_REPORT_STATUS = [
        ("PENDING", _('Pending')),
        ("DENIED", _('Denied')),
        ("APPROVED", _('Approved')),
        ("PAYED", _('Payed')),
        ("COMPLETED", _('Completed')),
        ("EXEMPTED", _('Exempted')),
    ]
    status = models.CharField(
        max_length=9,
        choices=MODULE_REGISTRATION_REPORT_STATUS,
        default="PENDING",
        verbose_name=_("Status")
    )

    class Meta:
        """Meta definition for ModuleRegistrationReport."""

        verbose_name = _('Module Registration Report')
        verbose_name_plural = _('Modules Registration Reports')

    # @property  # FIXME: School years from date_start and date_end
    # def school_year(self):
    #     """Compute the schoolyear of the module."""

    #     start = self.date_start
    #     end = self.date_end
    #     return start.strftime("%Y")

    @property
    def payed(self):
        """Check if the module registration request has been payed.

        A payed request is either payed or completed.
        """

        return self.status == "PAYED" or self.status == "COMPLETED"

    @property
    def approved(self):
        """Check if the module registration request has been approved.

        An approved request is either approved, payed or completed.
        """

        return self.status == "APPROVED" or self.payed

    @property
    def succeeded(self):
        """Check if the student succeeded the module modules.

        The module succeess is not valid if the student didn't payed his/her
        registration to it.
        """

        return self.status == "EXEMPTED" \
               or (self.status == "COMPLETED" and self.final_score >= 50)

    def __str__(self):
        """Unicode representation of ModuleRegistrationReport."""

        return "[{}] {}'s module registration for {} ({})".format(
            self.pk,
            self.student_rr.created_by.get_full_name(),
            self.module.title,
            self.status,
        )

    def get_absolute_url(self):
        """Return absolute url for DegreeRegistrationReport."""

        return reverse('module_rr_detailview', kwargs={"pk": self.pk})


@receiver(post_save, sender=DegreeRegistrationReport)
def generate_all_modules_rrs_of_degree_rr(sender, instance, **kwargs):
    """When a DegreeRegistrationReport is created, all the related
    ModuleRegistrationReports of the related modules are generated too and
    linked to the StudentRegistrationReport.

    NOTE: This couldn't be done in the DegreeRegistrationReport.save() because
    of a circular import issue.
    """

    for module in instance.degree.modules.all():
        for module_rr in module.modules_rrs.all():
            if module_rr.student_rr == instance.student_rr:
                if module_rr.status == "DENIED" or module_rr.status == "COMPLETED":
                    pass



        if module.modules_rrs.filter :
            pass
        else:
            pass
        ModuleRegistrationReport.objects.create(
            student_rr=instance.student_rr,
            degree_rr=instance,
            module=module,
        )
