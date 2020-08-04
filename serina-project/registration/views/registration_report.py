from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from django.views.generic import CreateView, DetailView, ListView

from ..forms import (
    ModuleRegistrationReportCreateFrom,
    StudentRegistrationReportCreateFrom,
)
from ..models import (
    DegreeRegistrationReport,
    ModuleRegistrationReport,
    StudentRegistrationReport,
)
from ..utils.groups import promote_to_student
from ..utils.messages import student_rr_created
from ..utils.mixins import (
    AutofillCreatedByRequestUser,
    ManagerAdministratorOnlyMixin,
)


# StudentRegistrationReport

class StudentRegistrationReportListView(
    LoginRequiredMixin,
    ManagerAdministratorOnlyMixin,
    ListView,
):  # TODO: Debug view
    """ListView for StudentRegistrationReports."""

    model = StudentRegistrationReport
    context_object_name = "student_rrs"
    template_name = "registration/registration_report/student_rr_listview." \
                    "html"


class StudentRegistrationReportDetailView(
    LoginRequiredMixin,
    ManagerAdministratorOnlyMixin,
    DetailView,
):  # TODO: Debug view
    """DetailView for StudentRegistrationReport."""

    # TODO: Restrict access to student who made student_rr
    model = StudentRegistrationReport
    context_object_name = "student_rr"
    template_name = "registration/registration_report/student_rr_detailview." \
                    "html"


class StudentRegistrationReportCreateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    CreateView,
    AutofillCreatedByRequestUser,
):  # TODO: Debug view
    """CreateView for StudentRegistrationReport.

    Only registered 'Guest'-group members can submit a
    StudentRegistrationReport. Once done, the 'Guest'-user is automatically
    promoted to the 'Student'-group.
    """

    model = StudentRegistrationReport
    form_class = StudentRegistrationReportCreateFrom
    template_name = "registration/registration_report/student_rr_createview." \
                    "html"

    def test_func(self):
        """Check if the user is a registered guest.

        Registered guest users are the only members who are allowed to submit a
        StudentRegistrationReport. The student cannot because they already did
        once. The other groups are not allowed to be student with the same
        account.
        """

        return self.request.user.groups.filter(name="Guest")

    def handle_no_permission(self):
        """Send an error message and redirect the home page."""

        if self.request.user.groups.filter(name="Student"):
            messages.error(
                self.request,
                _("You already submitted your registration report. To change "
                  "some of your data, please go to your profile and update "
                  "your peronal informations. Note that the submitted "
                  "documents and some data cannot be changed any more.")
            )
        else:
            messages.error(
                self.request,
                _("You are not allowed to submit a registration report. Please"
                  " create a new account.")
            )

        return redirect('home')

    def form_valid(self, form):
        """Promote the user to the 'Student'-group and notificate him/her with
        a message."""

        promote_to_student(self.request.user)
        student_rr_created(self.request)
        return super().form_valid(form)


# ModuleRegistrationReport

class ModuleRegistrationReportListView(
    LoginRequiredMixin,
    ManagerAdministratorOnlyMixin,
    ListView,
):  # TODO: Debug view
    """ListView for ModuleRegistrationReport."""

    model = ModuleRegistrationReport
    context_object_name = "modules_rrs"
    template_name = "registration/registration_report/module_rr_listview.html"

# TODO: Add ListView for student's modules_rrs only


class ModuleRegistrationReportDetailView(
    LoginRequiredMixin,
    ManagerAdministratorOnlyMixin,
    DetailView,
):  # TODO: Debug view
    """DetailView for ModuleRegistrationReport."""

    # TODO: Restrict access to student who made student_rr
    model = ModuleRegistrationReport
    context_object_name = "module_rr"
    template_name = "registration/registration_report/module_rr_detailview." \
                    "html"


class ModuleRegistrationReportCreateView(
    LoginRequiredMixin,
    CreateView,
    AutofillCreatedByRequestUser,
):  # TODO: Debug view
    """CreateView for ModuleRegistrationReport."""

    # TODO: Restrict access to student (because a student is a user whom submitted his student_rr)
    model = ModuleRegistrationReport
    # fields = '__all__'
    form_class = ModuleRegistrationReportCreateFrom
    template_name = "registration/registration_report/module_rr_createview." \
                    "html"

    def get_initial(self):
        """Returns the initial data to use for forms on this view."""

        initial = super().get_initial()
        initial['student_rr'] = self.request.user.student_rr
        return initial


class DegreeRegistrationReportListView(
    LoginRequiredMixin,
    ManagerAdministratorOnlyMixin,
    ListView,
):  # TODO: Debug view
    """ListView for DegreeRegistrationReportListView."""

    model = DegreeRegistrationReport
    context_object_name = "degrees_rrs"
    template_name = "registration/registration_report/degree_rr_listview.html"


class DegreeRegistrationReportDetailView(
    LoginRequiredMixin,
    ManagerAdministratorOnlyMixin,
    DetailView,
):  # TODO: Debug view
    """DetailView for DegreeRegistrationReportListView."""

    model = DegreeRegistrationReport
    context_object_name = "degree_rr"
    template_name = "registration/registration_report/degree_rr_detailview" \
                    ".html"
