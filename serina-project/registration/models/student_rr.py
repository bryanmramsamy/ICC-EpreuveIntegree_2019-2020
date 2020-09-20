from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.shortcuts import reverse
from django.utils.translation import ugettext as _

from . import resource


class StudentRegistrationReport(resource.FrontOfficeResource):
    """Model definition for StudentRegistrationReport.

    Report containing all the information related to a guest registered user
    whom wants to be promoted as a student in order to follow his/her wished
    degree(s) and/or module(s).
    """

    created_by = models.OneToOneField(  # TODO: Add validator: guest/student
        User,
        on_delete=models.CASCADE,
        related_name="student_rr",
        verbose_name=_("Student"),
    )
    birthday = models.DateField(verbose_name=_("Birthday date"))
    nationality = models.CharField(max_length=50,
                                   verbose_name=_("Nationality"))
    address = models.CharField(max_length=255, verbose_name=_("Address"))
    additional_address = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Additional address"),
    )
    postal_code = models.CharField(max_length=50,
                                   verbose_name=_("Postal code"))
    postal_locality = models.CharField(max_length=50,
                                       verbose_name=_("Locality"))

    # Student files

    # TODO: Add upload_to argument

    id_picture = models.ImageField(verbose_name=_("ID picture"))
    # TODO: Add validators to accept pdf files only
    # https://stackoverflow.com/questions/6460848/how-to-limit-file-types-on-file-uploads-for-modelforms-with-filefields
    id_card = models.FileField(verbose_name=_("ID card"))
    secondary_education_certificate = models.FileField(
        verbose_name=_("Secondary Education Certificate")
    )
    annex_403 = models.FileField(
        null=True,
        blank=True,
        verbose_name=_("Annex 403")
    )
    other_school_inscription_certificate = models.FileField(
        null=True,
        blank=True,
        verbose_name=_("Other schools inscription certificate")
    )
    national_register_extract = models.FileField(
        null=True,
        blank=True,
        verbose_name=_("National Register Extract")
    )
    belgian_studies_history = models.FileField(
        null=True,
        blank=True,
        verbose_name=_("Belgian Studies History")
    )
    archievement_certificates = models.FileField(
        null=True,
        blank=True,
        verbose_name=_("Modules archievement certificates")
    )
    job_organization_certificates = models.FileField(
        null=True,
        blank=True,
        verbose_name=_("Job organizations certificates")
    )
    exemption_report = models.FileField(  # TODO: Add validator: only zip file
        null=True,
        blank=True,
        verbose_name=_("Exemption reports")
    )

    class Meta:
        """Meta definition for StudentRegistrationReport."""

        verbose_name = _('Student registration report')
        verbose_name_plural = _('Student registration reports')

    @property
    def all_modules_approved(self):
        """Check if all the modules_rrs were approved."""

        modules_approved = True

        for module_rr in self.modules_rrs.all():
            if not module_rr.approved:
                modules_approved = False
                break

        return modules_approved

    @property
    def all_modules_payed(self):
        """Check if all the approved modules_rrs were payed."""

        modules_payed = True

        for module_rr in self.modules_rrs.all():
            if module_rr.approved and not module_rr.payed:
                modules_payed = False
                break

        return modules_payed

    @property
    def total_expenses(self):
        """Compute the total registration expenses of the student."""

        total_expenses = 0
        for module_rr in self.modules_rrs.all():
            total_expenses += module_rr.module.charge_price

        return total_expenses

    @property
    def success_rate(self):
        """Compute the success rate of the student.

        The success rate is the amount of succeeded modules divided by the
        total followed modules.
        """

        succeeded_modules = 0
        total_modules = 0

        for module_rr in self.modules_rrs.all():
            total_modules += 1

            if module_rr.succeeded:
                succeeded_modules += 1

        success_rate = succeeded_modules / total_modules * 100
        return "{}%".format(success_rate)

    @property
    def spent_ECTS(self):
        """Compute the total amount of spent ECTS.

        The ECTS is the value measurment of a module.
        When a student register to a module, (s)he must pay with his/her ECTS.
        """

        spent_ECTS = 0

        for module_rr in self.modules_rrs.all():
            if module_rr.payed:
                spent_ECTS += module_rr.module.ECTS_value

        return spent_ECTS

    @property
    def won_ECTS(self):
        """Compute the total amount of won ECTS.

        The ECTS is the value measurment of a module.
        When a student succeed a module, (s)he get his/her ECTS back.
        """

        won_ECTS = 0

        for module_rr in self.modules_rrs.all():
            if module_rr.succeeded and module_rr.payed:
                won_ECTS += module_rr.module.ECTS_value

        return won_ECTS

    @property
    def average_score(self):
        """Compute the average final score of the student."""

        return resource.modules_average_score(self)

    @property
    def has_been_student(self):
        """Check if the user was registered as student for at least one
        module.
        """

        return self.modules_rrs.count() > 0

    @property
    def has_graduated(self):
        """Check if the studend did graduate for a degree at least once."""

        pass

    def __str__(self):
        """Unicode representation of StudentRegistrationReport."""

        return "[{}] {}'s student registration report".format(
            self.pk,
            self.created_by.get_full_name(),
        )

    # TODO: Must be defined
    # def clean(self):
    #     """Clean method for StudentRegistrationReport.

    #     Check if the user is a guest or a student, if the student is not
    #     underaged and if the uploaded files are on the correct format.
    #     """

    #     pass

    def get_absolute_url(self):
        """Return absolute url for StudentRegistrationReport."""

        return reverse("student_rr_detailview", kwargs={"pk": self.pk})


# def user_directory_path(instance, filename):
#     return "{}-{}.{}/{}".format(
#         instance.user.username,
#         instance.user.first_name,
#         instance.user.last_name,
#         filename,
#     )

# class MyModel(models.Model):
#     upload = models.FileField(upload_to=user_directory_path)