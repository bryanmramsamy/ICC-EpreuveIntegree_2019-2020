from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from django.views.generic import CreateView, DetailView, ListView

from ..forms import (
    DegreeRegistrationReportCreateFrom,
    ModuleRegistrationReportCreateFrom,
    StudentRegistrationReportCreateFrom,
)
from ..models import (
    DegreeRegistrationReport,
    ModuleRegistrationReport,
    StudentRegistrationReport,
)
from ..utils import (
    groups as groups_utils,
    messages as messages_utils,
    mixins as mixins_utils,
)


# StudentRegistrationReport

class StudentRegistrationReportListView(
    LoginRequiredMixin,
    mixins_utils.ManagerAdministratorOnlyMixin,
    ListView,
):  # TODO: Debug view
    """ListView for StudentRegistrationReports."""

    model = StudentRegistrationReport
    context_object_name = "student_rrs"
    template_name = "registration/registration_report/student_rr_listview." \
                    "html"


class StudentRegistrationReportDetailView(
    LoginRequiredMixin,
    mixins_utils.SelfStudentManagerAdministratorOnlyMixin,
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
    mixins_utils.AutofillCreatedByRequestUser,
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
            messages_utils.student_rr_already_created(self.request,
                                                      self.request.user)
        else:
            messages_utils.permission_denied(self.request)

        return redirect('home')

    def form_valid(self, form):
        """Promote the user to the 'Student'-group and notificate him/her with
        a message."""

        groups_utils.promote_to_student(self.request.user)
        messages_utils.student_rr_created(self.request)
        return super().form_valid(form)


# ModuleRegistrationReport

class ModuleRegistrationReportListView(
    LoginRequiredMixin,
    mixins_utils.ManagerAdministratorOnlyMixin,
    ListView,
):  # TODO: Debug view
    """ListView for ModuleRegistrationReport."""

    model = ModuleRegistrationReport
    context_object_name = "modules_rrs"
    template_name = "registration/registration_report/module_rr_listview.html"

# TODO: Add ListView for student's modules_rrs only


class ModuleRegistrationReportDetailView(
    LoginRequiredMixin,
    mixins_utils.SelfStudentManagerAdministratorOnlyMixin,
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
    mixins_utils.AutofillCreatedByRequestUser,
):  # TODO: Debug view
    """CreateView for ModuleRegistrationReport."""

    # TODO: Restrict access to student (because a student is a user whom submitted his student_rr)
    model = ModuleRegistrationReport
    form_class = ModuleRegistrationReportCreateFrom
    template_name = "registration/registration_report/module_rr_createview." \
                    "html"

    def get_initial(self):
        """Returns the initial data to use for forms on this view."""

        initial = super().get_initial()
        initial['student_rr'] = self.request.user.student_rr
        return initial


# DegreeRegistrationReport

class DegreeRegistrationReportListView(
    LoginRequiredMixin,
    mixins_utils.ManagerAdministratorOnlyMixin,
    ListView,
):  # TODO: Debug view
    """ListView for DegreeRegistrationReportListView."""

    model = DegreeRegistrationReport
    context_object_name = "degrees_rrs"
    template_name = "registration/registration_report/degree_rr_listview.html"


class DegreeRegistrationReportDetailView(
    LoginRequiredMixin,
    mixins_utils.SelfStudentManagerAdministratorOnlyMixin,
    DetailView,
):  # TODO: Debug view
    """DetailView for DegreeRegistrationReportListView."""

    model = DegreeRegistrationReport
    context_object_name = "degree_rr"
    template_name = "registration/registration_report/degree_rr_detailview" \
                    ".html"


class DegreeRegistrationReportCreateView(
    LoginRequiredMixin,
    CreateView,
    mixins_utils.AutofillCreatedByRequestUser,
):  # TODO: Debug view
    """CreateView for DegreeRegistrationReport."""

    # TODO: Restrict access to student (because a student is a user whom submitted his student_rr)
    model = DegreeRegistrationReport
    form_class = DegreeRegistrationReportCreateFrom
    template_name = "registration/registration_report/degree_rr_createview." \
                    "html"

    def get_initial(self):
        """Returns the initial data to use for forms on this view."""

        initial = super().get_initial()
        initial['student_rr'] = self.request.user.student_rr
        return initial
