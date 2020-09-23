from django.conf import settings
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
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="modules_rrs",
        verbose_name=_("Course")
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
    exemption_request = models.BooleanField(
        default=False,
        verbose_name=_("Student exemption request"),
        help_text=_(
            "If you already succeeded this or a similar module in another "
            "school or educational organization, you can ask for an "
            "exemption. This will prevent you from passing paying this module "
            "if your request is accepted by our staff."
        ),
    )
    exemption_report = models.FileField(  # TODO: Add validator: only zip file
        null=True,
        blank=True,
        verbose_name=_("Exemption reports"),
        help_text=_(
            "Send the documents that can provide you a exemption for this "
            "module. The documents will be verified by our staff and help "
            "them taking a decision regarding your request."
        ),
    )

    STATUS = [
        ("PENDING", _('Pending')),
        ("DENIED", _('Denied')),
        ("APPROVED", _('Approved')),
        ("PAYED", _('Payed')),
        ("COMPLETED", _('Completed')),
        ("EXEMPTED", _('Exempted')),
    ]
    status = models.CharField(
        max_length=9,
        choices=STATUS,
        default="PENDING",
        verbose_name=_("Status")
    )

    class Meta:
        """Meta definition for ModuleRegistrationReport."""

        verbose_name = _('Module Registration Report')
        verbose_name_plural = _('Modules Registration Reports')

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
    def success_score_threshold_reached(self):
        """Check if the final score is above the success score threshold."""

        return self.final_score >= settings.SUCCESS_SCORE_THRESHOLD

    @property
    def succeeded(self):
        """Check if the student succeeded the module modules.

        The module succeess is not valid if the student didn't payed his/her
        registration to it.
        """

        return (self.status == "EXEMPTED" or self.status == "COMPLETED") \
            and self.success_score_threshold_reached

    def __str__(self):
        """Unicode representation of ModuleRegistrationReport."""

        return "[{}] {}'s module registration for {} ({})".format(
            self.pk,
            self.student_rr.created_by.get_full_name(),
            self.module.title,
            self.status,
        )

    def clean(self):
        """Clean method for ModuleRegistrationReport.

        Check if the user is a guest or a student, if the student is not
        underaged and if the uploaded files are on the correct format.
        """

        if (self.status == "COMPLETED" or self.status == "EXEMPTED") \
           and not self.final_score:
            raise ValidationError(_(
                "The Module Registration Request cannot be flagged as "
                "completed nor exempted if no final score was given."
            ))

        if not (self.approved or self.status == "EXEMPTED") \
           and self.final_score:
            raise ValidationError(_(
                "You cannot put a final score to a registration which is not "
                "approved."
            ))

        if self.status == "EXEMPTED" and not self.succeeded:
            raise ValidationError(_(
                "If a module is exempted, the final score must be equal or "
                "above the success score threshold, which is actually at {}."
                .format(settings.SUCCESS_SCORE_THRESHOLD)
            ))

        if self.payed and not self.date_payed:
            raise ValidationError(_(
                "The Module Registration Request cannot be flagged as "
                "payed nor completed if no payment date was entered."
            ))

    def get_absolute_url(self):
        """Return absolute url for ModuleRegistrationReport."""

        return reverse('module_rr_detailview', kwargs={"pk": self.pk})


@receiver(post_save, sender=DegreeRegistrationReport)  # TODO: Review this
def generate_all_modules_rrs_of_degree_rr(sender, instance, **kwargs):
    """When a DegreeRegistrationReport is created, all the related
    ModuleRegistrationReports of the related modules are generated too and
    linked to the StudentRegistrationReport.

    NOTE: This couldn't be done in the DegreeRegistrationReport.save() because
    of a circular import issue.
    """
    # FIXME: A new module_rr must be created for each module of the degree_rr, if a previous module_rr validated exists, the user should should be prompted to ignore it (default, module_rr wil be flagged as EXEMPTED and best final_score available will be taken over) or redo it.

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
