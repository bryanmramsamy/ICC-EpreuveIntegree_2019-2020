from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import (
    FileExtensionValidator,
    MaxValueValidator,
    MinValueValidator,
)
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
    invoice_id = models.CharField(
        null=True,
        max_length=16,
        verbose_name=_("Invoice ID"),
    )
    payed_fees = models.DecimalField(
        default=0,
        max_digits=5,
        decimal_places=2,
        verbose_name=_('Payed fees'),
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
    exemption_report = models.FileField(
        null=True,
        blank=True,
        validators=[FileExtensionValidator(
            allowed_extensions=['pdf', 'zip', 'jpeg', 'jpg', 'png'],
        )],
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
    def approved(self):
        """True is the module registration was at least approved.

        True if the request status is in the followinf list:
        ['APPROVED', 'PAYED', 'COMPLETED']
        """

        return self.status == "APPROVED" or self.payed

    @property
    def approved_or_exempted(self):
        """True is the module registration was at least approved or exempted.

        True if the request status is in the followinf list:
        ['APPROVED', 'PAYED', 'COMPLETED', 'EXEMPTED']
        """

        return self.status == "EXEMPTED" or self.approved

    @property
    def payed(self):
        """True is the module registration was at least payed.

        True if the request status is in the followinf list:
        [PAYED', 'COMPLETED']
        """

        return self.status == "PAYED" or self.status == "COMPLETED"

    @property
    def payed_or_exempted(self):
        """True is the module registration was at least payed or exempted.

        True if the request status is in the followinf list:
        ['PAYED', 'COMPLETED', 'EXEMPTED']
        """

        return self.status == "EXEMPTED" or self.payed

    @property
    def finished(self):
        """True if the module registration is either completed or exempted, no
        regardless of the student having succeeded or not.

        True if the request status is in the followinf list:
        ['COMPLETED', 'EXEMPTED']
        """

        return self.status == "COMPLETED" or self.status == "EXEMPTED"

    @property
    def success_score_threshold_reached(self):
        """True if the final score is equal or above the defined success score
        threshold."""

        return self.final_score >= settings.SUCCESS_SCORE_THRESHOLD

    @property
    def succeeded(self):
        """Check if the student succeeded the module modules.

        The module succeess is not valid if the student didn't payed his/her
        registration to it.
        """

        return (self.status == "EXEMPTED" or self.status == "COMPLETED") \
            and self.success_score_threshold_reached

    @property
    def to_be_payed_fees(self):
        """Calculate the amount still to be payed by the student based on the
        module price and the payed_fees. This is only computed when the module
        registration report has the 'APPROVED' status."""

        return self.module.price - self.payed_fees

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

        if self.payed and not self.date_payed:
            raise ValidationError(_(
                "The Module Registration Request cannot be flagged as "
                "payed nor completed if no payment date was entered."
            ))

        if not self.approved_or_exempted and self.final_score:
            raise ValidationError(_(
                "You cannot put a final score to a registration which is not "
                "approved."
            ))

        if (self.status == "COMPLETED" or self.status == "EXEMPTED") \
           and not self.final_score:
            raise ValidationError(_(
                "The Module Registration Request cannot be flagged as "
                "completed nor exempted if no final score was given."
            ))

        if self.status == "EXEMPTED" and not success_score_threshold_reached:
            raise ValidationError(_(
                "If a module is exempted, the final score must be equal or "
                "above the success score threshold, which is actually at {}."
                .format(settings.SUCCESS_SCORE_THRESHOLD)
            ))

    def save(self, *args, **kwargs):
        """Save the unique invoice ID on creation."""

        if not self.pk:
            self.invoice_id = "#" + self.student_rr.created_by.username + "M"
            super().save(*args, **kwargs)
            self.invoice_id += str(self.pk).zfill(5)

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Return absolute url for ModuleRegistrationReport."""

        return reverse('module_rr_detailview', kwargs={"pk": self.pk})
