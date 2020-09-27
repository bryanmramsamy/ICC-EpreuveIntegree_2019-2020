from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models import Q
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
        on_delete=models.CASCADE,
        related_name="students_registrations",
        verbose_name=_("Registration degree")
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
        """Check if at least one of the related modules_rr is pending."""

        if self.modules_rrs.all().count() > 0:
            partially_pending = self.modules_rrs.filter(status="PENDING")\
                                                .exists()

        return partially_pending

    @property
    def fully_pending(self):
        """Check if all the related modules_rr are pending."""

        if self.modules_rrs.all().count() > 0:
            fully_pending = self.modules_rrs.exclude(status="PENDING").exists()

        # FIXME: See note in student_graduated

        return fully_pending

    @property
    def partially_denied(self):
        """Check if at least one of the related modules_rr is denied."""

        if self.modules_rrs.all().count() > 0:
            partially_denied = self.modules_rrs.filter(
                Q(status="DENIED") | ~Q(status="EXEMPTED")).exists()

        return partially_denied

    @property
    def fully_denied(self):
        """Check if all the related modules_rr are denied."""

        if self.modules_rrs.all().count() > 0:
            fully_denied = self.modules_rrs.exclude(
                Q(status="DENIED") | Q(status="EXEMPTED")
            ).exists()

        # FIXME: See note in student_graduated

        return fully_denied

    @property
    def partially_approved(self):
        """Check if at least one of the related modules_rr is approved.

        Return 'None' if there is no modules_rrs in the degree_rr.
        """

        if self.modules_rrs.all().count() > 0:
            partially_approved = True in [module_rr.approved for module_rr in
                                          self.modules_rrs.all()]

        return partially_approved

    @property
    def fully_approved(self):
        """Check if all the related modules_rr are approved.

        Return 'None' if there is no modules_rrs in the degree_rr.
        """

        if self.modules_rrs.all().count() > 0:
            fully_approved = not (False in [module_rr.approved for module_rr in
                                            self.modules_rrs.all()])

        # FIXME: See note in student_graduated

        return fully_approved

    @property
    def partially_payed(self):
        """Check if at least one of the related modules_rr is approved.

        Return 'None' if there is no modules_rrs in the degree_rr.
        """

        if self.modules_rrs.all().count() > 0:
            partially_payed = True in [module_rr.payed for module_rr in
                                       self.modules_rrs.all()]

        return partially_payed

    @property
    def fully_payed(self):
        """Check if all the related modules_rr are payed.

        Return 'None' if there is no modules_rrs in the degree_rr.
        """

        if self.modules_rrs.all().count() > 0:
            fully_payed = not (False in [module_rr.payed for module_rr in
                                         self.modules_rrs.all()])
        # FIXME: See note in student_graduated


        return fully_payed

    @property
    def student_graduated(self):
        """Check if the student succeeded all the degree's modules."""

        if self.modules_rrs.all().count() > 0:
            fully_succeeded = not (False in [module_rr.succeeded for module_rr
                                             in self.modules_rrs.all()])
        # FIXME: What if student fails, resubscribe to module and succeed ?
        # He will accomplish every module, but the fail still count and degree
        # won't be succeeded
        # NOTE: Must loop on each module and on each rr of these
        # NOTE: Use query instead of for-loops if possible

        return fully_succeeded

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

        return total_paid_price if total_paid_price > 0 else -1

    def __str__(self):
        """Unicode representation of DegreeRegistrationRapport."""

        return "[{}] {}'s degree registration for {}".format(
            self.pk,
            self.student_rr.created_by.get_full_name(),
            self.degree.title,
        )

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
