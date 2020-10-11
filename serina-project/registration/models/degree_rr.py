from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models import Sum, Q
from django.db.models.signals import post_save
from django.dispatch import receiver
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
        null=True,
        on_delete=models.SET_NULL,
        related_name="students_registrations",
        verbose_name=_("Registration degree")
    )
    invoice_id = models.CharField(
        unique=True,
        editable=False,
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
    exemption_request = models.BooleanField(
        default=False,
        verbose_name=_("Student exemption request"),
        help_text=_(
            "If you already succeeded this or a similar module part of this "
            "degree in another school or educational organization, you can "
            "ask for an exemption. This will prevent you from passing paying "
            "this module if your request is accepted by our staff."
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
            "Send the documents that can provide you a exemption for one or "
            "miltiple modules of this degree. The documents will be verified "
            "by our staff and help them taking a decision regarding your "
            "request."
        ),
    )

    class Meta:
        """Meta definition for DegreeRegistrationReport."""

        verbose_name = _('Degree Registration Report')
        verbose_name_plural = _('Degrees Registration Reports')

    @property
    def partially_pending(self):
        """True if at least one of the related modules_rr is pending."""

        from ..utils import registration as registration_utils

        return registration_utils.degree_rr_is_partially_pending(self)

    @property
    def fully_pending(self):
        """True if all the related modules_rr are pending."""

        from ..utils import registration as registration_utils

        return registration_utils.degree_rr_is_fully_pending(self)

    @property
    def partially_denied(self):
        """True if at least one of the related modules_rr is denied."""

        from ..utils import registration as registration_utils

        return registration_utils.degree_rr_is_partially_denied(self)

    @property
    def fully_denied(self):
        """True if all the related modules_rr are denied."""

        from ..utils import registration as registration_utils

        return registration_utils.degree_rr_is_partially_denied(self)

    @property
    def partially_approved(self):
        """Check if at least one of the related modules_rr is approved."""

        from ..utils import registration as registration_utils

        return registration_utils.degree_rr_is_partially_approved(self)

    @property
    def fully_approved(self):
        """True if all the related modules_rr are approved."""

        from ..utils import registration as registration_utils

        return registration_utils.degree_rr_is_fully_approved(self)

    @property
    def partially_payed(self):
        """True if at least one of the related modules_rr is payed."""

        from ..utils import registration as registration_utils

        return registration_utils.degree_rr_is_partially_payed(self)

    @property
    def fully_payed(self):
        """True if all the related modules_rr are payed."""

        from ..utils import registration as registration_utils

        return registration_utils.degree_rr_is_fully_payed(self)

    @property
    def status(self):
        """Return the status of the degree according to the statuses of all the
        related module registration reports.

        Priority order of the statuses:
        * FULLY_DENIED: All the modules has been denied
        * PARTIALLY_DENIED: At least one module has been denied
        * COMPLETED: At least one of each module has been succeeded
        * FULLY_PAYED: All the modules has been payed
        * PARTIALLY_PAYED: At least one module has been payed
        * FULLY_APPROVED: All the modules has been approved
        * PARTIALLY_APPROVED: At least one module has been approved
        * FULLY_DENIED: All the modules are still pending
        * PARTIALLY_DENIED: At least one module is still pending
        """

        from ..utils import registration as registration_utils

        if registration_utils.degree_rr_is_fully_denied(self):
            status = "FULLY_DENIED"

        elif registration_utils.degree_rr_is_partially_denied(self):
            status = "PARTIALLY_DENIED"

        elif registration_utils.degree_rr_is_completed(self):
            status = "COMPLETED"

        elif registration_utils.degree_rr_is_fully_payed(self):
            status = "FULLY_PAYED"

        elif registration_utils.degree_rr_is_partially_payed(self):
            status = "PARTIALLY_PAYED"

        elif registration_utils.degree_rr_is_fully_approved(self):
            status = "FULLY_APPROVED"

        elif registration_utils.degree_rr_is_partially_approved(self):
            status = "PARTIALLY_APPROVED"

        elif registration_utils.degree_rr_is_fully_pending(self):
            status = "FULLY_PENDING"

        elif registration_utils.degree_rr_is_partially_pending(self):
            status = "PARTIALLY_PENDING"

        else:
            status = None

        return status

    @property
    def approved(self):
        """True if the degree registration report has one of the following
        statuses: ['FULLY_APPROVED', 'PARTIALLY_PAYED', 'FULLY_PAYED',
                   'COMPLETED']."""

        return self.status == 'FULLY_APPROVED' \
            or self.status == 'PARTIALLY_PAYED' \
            or self.status == 'FULLY_PAYED' \
            or self.status == 'COMPLETED'

    @property
    def payed(self):
        """True if the degree registration report has one of the following
        statuses: ['FULLY_PAYED', 'COMPLETED']."""

        return self.status == 'FULLY_PAYED' or self.status == 'COMPLETED'

    @property
    def graduated(self):
        """Check if the student succeeded all the degree's modules."""

        from ..utils import registration as registration_utils

        return registration_utils.degree_rr_is_completed(self)

    @property
    def average_score(self):
        """Compute the average score of the student."""

        return resource.modules_average_score(self)

    @property
    def total_fees(self):
        """Sum of the costs of each module of the degree related to the degree
        registration report.

        The denied and exempted modules are excluded.
        """

        return self.modules_rrs.exclude(
            Q(status="DENIED") | Q(status="EXEMPTED")
        ).aggregate(Sum('module__price'))["module__price__sum"]

    @property
    def to_be_payed_fees(self):
        """Calculate the amount still to be payed by the student based on the
        module price and the payed_fees. This is only computed when the module
        registration report has the 'APPROVED' status."""

        return self.total_fees - self.payed_fees

    def __str__(self):
        """Unicode representation of DegreeRegistrationRapport."""

        return "[{}] {}'s degree registration for {}".format(
            self.pk,
            self.student_rr.created_by.get_full_name(),
            self.degree.title,
        )

    def save(self, *args, **kwargs):
        """Save the unique invoice ID on creation."""

        if not self.pk:
            self.invoice_id = "#" + self.student_rr.created_by.username + "D"

            super().save(*args, **kwargs)

            self.invoice_id += str(self.pk).zfill(5)

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Return absolute url for DegreeRegistrationRappport."""

        return reverse("degree_rr_detailview", kwargs={"pk": self.pk})


@receiver(post_save, sender=DegreeRegistrationReport)
def generate_all_modules_rrs_of_degree_rr(sender, instance, created, **kwargs):
    """Create all the Module Registration Reports for each module of the
    degree from the given Degree Registration Report.

    If a Module Registration Report already validated or exempted already
    exists for a specific module, a new report will be created and flagged as
    'EXEMPTED'. The final score will be repported as well.
    """

    from ..utils import registration as registration_utils

    if created:
        registration_utils.create_modules_rrs_for_degree_rr(instance)
