from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.shortcuts import reverse
from django.utils.translation import ugettext as _

from management.models import Course, Degree, Module


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


class StudentRegistrationReport(FrontOfficeResource):
    """Model definition for StudentRegistrationReport.

    Report containing all the information related to a guest registered user
    whom wants to be promoted as a student in order to follow his/her wished
    degree(s) and/or module(s).
    """

    user = models.OneToOneField(  # TODO: Add validator: guest/student
        User,
        on_delete=models.CASCADE,
        related_name="student_registration_report",
        verbose_name=_("Student"),
    )
    birthday = models.DateField(verbose_name=_("Birthday date"))
    nationality = models.CharField(max_length=50,
                                   verbose_name=_("Nationality"))
    address = models.CharField(max_length=255, verbose_name=_("Address"))
    additional_address = models.CharField(max_length=255,
                                          verbose_name=_("Additional address"))
    postal_code = models.CharField(max_length=50,
                                   verbose_name=_("Postal code"))
    postal_locality = models.CharField(max_length=50,
                                       verbose_name=_("Locality"))

    # Student files

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
        verbose_name=_("Other schools inscription certificate"))
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
        verbose_name=_("Modules archievement certificates"))
    job_organization_certificates = models.FileField(
        null=True,
        blank=True,
        verbose_name=_("Job organizations certificates"))
    exemption_report = models.FileField(  # TODO: Add validator: only zip file
        null=True,
        blank=True,
        verbose_name=_("Exemption reports")
    )

    class Meta:
        """Meta definition for StudentRegistrationReport."""

        verbose_name = _('Student registration report')
        verbose_name_plural = _('Student registration reports')

    # TODO: Must be defined when DegreeRegistrationReport and
    #       ModuleRegistrationReport will be defined
    # @property
    # def total_expenses(self):
    #     """Compute the total registration expenses of the student."""

    #     pass

    # TODO: Must be defined when DegreeRegistrationReport and
    #       ModuleRegistrationReport will be defined
    # @property
    # def success_rate(self):
    #     """Compute the success rate of the student.
    # 
    #     The success rate is the amount of succeeded modules divided by the total followed modules.
    #     """

    #     pass

    # TODO: Must be defined when DegreeRegistrationReport and
    #       ModuleRegistrationReport will be defined
    # @property
    # def avg_score(self):
    #     """Compute the average final score of the student."""

    #     pass

    # TODO: Must be defined when DegreeRegistrationReport and
    #       ModuleRegistrationReport will be defined
    # @property
    # def has_been_student(self):
    #     """Check if the user was registered as student for at least one
    #     module.
    #     """

    #     pass

    # TODO: Must be defined when DegreeRegistrationReport and
    #       ModuleRegistrationReport will be defined
    # @property
    # def has_graduated(self):
    #     """Check if the studend did graduated for a degree at least once."""

    #     pass

    def __str__(self):
        """Unicode representation of StudentRegistrationReport."""

        return "[{}] {}'s student registration report".format(
            self.pk,
            self.self.user.get_full_name,
        )

    # TODO: Must be defined
    # def clean(self):
    #     """Clean method for StudentRegistrationReport.

    #     Check if the user is a guest or a student, if the student is not
    #     underaged and if the uploaded files are on the correct format.
    #     """

    #     pass

    # TODO: Must be define and redirect to Student Report's template
    # def get_absolute_url(self):
    #     """Return absolute url for StudentRegistrationReport."""
    #     return ('')


# def user_directory_path(instance, filename):
#     return "{}-{}.{}/{}".format(
#         instance.user.username,
#         instance.user.first_name,
#         instance.user.last_name,
#         filename,
#     )

# class MyModel(models.Model):
#     upload = models.FileField(upload_to=user_directory_path)

class DegreeRegistrationReport(FrontOfficeResource):
    """Model definition for DegreeRegistrationReport.

    Degree Registration Report of a degree to which the student registered.
    Contains all the related data of the student progression in the degree.
    """

    # TODO: Add FK on self from ModuleRegistrationReport
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

    # TODO: Must be defined when ModuleRegistrationReport will be defined
    # @property
    # def student_graduated(self):
    #     """Check if the student succeeded all the degree's modules."""

    #     pass

    # TODO: Must be defined when ModuleRegistrationReport will be defined
    # @property
    # def average_score(self):
    #     """Compute the average score of the student."""

    #     pass

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


class ModuleRegistrationReport(FrontOfficeResource):
    """Model definition for ModuleRegistrationReport.

    Model Registration Report of a model to which the student registered.
    Contains all the related data of the student progression in the module.
    """

    student_registration_report = models.ForeignKey(
        StudentRegistrationReport,
        on_delete=models.CASCADE,
        related_name="modules_registration_reports",
        verbose_name=_("Student"),)
    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name="students_registrations",
        verbose_name=_("Registration module")
    )
    course =  models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="students_registrations",
        verbose_name=_("Course")
    )
    degree_registration_report = models.ForeignKey(
        DegreeRegistrationReport,
        null=True,  # TODO: Confirm if blank=True is not needed
        on_delete=models.CASCADE,
        related_name="modules_registration_reports",
        verbose_name=_("Degree Registration Report")
    )
    date_start = models.DateField(verbose_name=_("Start date"))
    date_end = models.DateField(verbose_name=_("End date"))
    student_attempt = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Student's attempt number")
    )  # TODO: Add max_attempt value from settings
    student_final_score = models.FloatField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name=_("Final score"))
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

        return self.payed and self.student_final_score >= 50

    def __str__(self):
        """Unicode representation of ModuleRegistrationReport."""

        return "[{}] {}'s module registration for {}".format(
            self.pk,
            self.student_registration_report.user.get_full_name(),
            self.module.title,
        )

    # TODO: Must be define and redirect to Student Degree's Report template
    # def get_absolute_url(self):
    #     """Return absolute url for DegreeRegistrationRappport."""

    #     return ('')
