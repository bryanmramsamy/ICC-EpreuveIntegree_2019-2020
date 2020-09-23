from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import ugettext as _
from django.views.generic import CreateView, DetailView, ListView

from ..forms import (
    DegreeRegistrationReportCreateFrom,
    ModuleRegistrationReportCreateFrom,
    StudentRegistrationReportCreateFrom,
    SubmitFinalScoreForm,
)
from ..models import (
    DegreeRegistrationReport,
    ModuleRegistrationReport,
    StudentRegistrationReport,
)
from ..utils import (
    groups as groups_utils,
    management as management_utils,
    messages as messages_utils,
    mixins as mixins_utils,
    registration as registration_utils,
)
from management import models


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

    model = StudentRegistrationReport
    context_object_name = "student_rr"
    template_name = "registration/registration_report/student_rr_detailview." \
                    "html"


class StudentRegistrationReportCreateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    CreateView,
    mixins_utils.AutofillCreatedByRequestUser,
):
    """CreateView for HomegrownStudentRegistrationReport.

    Only registered 'Guest'-group members can submit a
    StudentRegistrationReport. Once done, the 'Guest'-user is automatically
    promoted to the 'Student'-group.
    """

    model = StudentRegistrationReport
    form_class = StudentRegistrationReportCreateFrom
    template_name = "registration/registration_report/student_rr_createview" \
                    ".html"

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

        raise PermissionDenied

    def form_valid(self, form):
        """Promote the user to the 'Student'-group and notificate him/her with
        a message."""

        groups_utils.promote_to_student(self.request.user)
        messages_utils.student_rr_created(self.request)
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        """Add foreign student flag to view in order hide/show foreign
        student's additional fields to fill."""

        context = super().get_context_data(*args, **kwargs)
        context["support_team_mail"] = settings.CONTACT_MAILS["support"]
        context["foreign_form"] = False

        return context


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


class ModuleRegistrationReportDetailView(
    LoginRequiredMixin,
    mixins_utils.SelfStudentBackOfficeUsersOnlyMixin,
    DetailView,
):
    """DetailView for ModuleRegistrationReport."""

    model = ModuleRegistrationReport
    context_object_name = "module_rr"
    template_name = "registration/registration_report/module_rr_detailview." \
                    "html"

    def get_context_data(self, **kwargs):
        """Add score submission form to context for back-office user only."""

        context = super().get_context_data(**kwargs)

        if groups_utils.is_back_office_user(self.request.user):
            context["form"] = SubmitFinalScoreForm

            if self.get_object().final_score:
                context['form_final_score'] = self.get_object().final_score

            if self.get_object().notes:
                context['form_notes'] = self.get_object().notes

        return context


class ModuleRegistrationReportCreateView(
    LoginRequiredMixin,
    mixins_utils.StudentOnlyMixin,
    CreateView,
    mixins_utils.AutofillCreatedByRequestUser,
):
    """CreateView for ModuleRegistrationReport."""

    model = ModuleRegistrationReport
    form_class = ModuleRegistrationReportCreateFrom
    template_name = "registration/registration_report/module_rr_createview." \
                    "html"

    def get_initial(self):
        """Returns the initial data to use for forms on this view."""

        initial = super().get_initial()
        initial['student_rr'] = self.request.user.student_rr
        initial['module'] = get_object_or_404(models.Module,
                                              pk=self.kwargs["module_pk"])
        return initial

    def get_context_data(self, **kwargs):
        """Add check variables for template conditions."""

        context = super().get_context_data(**kwargs)
        context["module"] = get_object_or_404(models.Module,
                                              pk=self.kwargs["module_pk"])
        context["active_module_rr_already_exists"] = \
            registration_utils.active_module_rr_already_exists(
                self.request.user,
                context["module"],
            )
        context["succeeded_module_rr_already_exists"] = \
            registration_utils.succeeded_module_rr_already_exists(
                self.request.user,
                context["module"],
            )
        return context


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
    # mixins_utils.StudentOnlyMixin,  # TODO: Disabled for debug purposes
    CreateView,
    mixins_utils.AutofillCreatedByRequestUser,
):  # TODO: Debug view
    """CreateView for DegreeRegistrationReport."""

    model = DegreeRegistrationReport
    form_class = DegreeRegistrationReportCreateFrom
    template_name = "registration/registration_report/degree_rr_createview." \
                    "html"

    def get_initial(self):
        """Returns the initial data to use for forms on this view."""

        initial = super().get_initial()
        initial['student_rr'] = self.request.user.student_rr
        return initial
