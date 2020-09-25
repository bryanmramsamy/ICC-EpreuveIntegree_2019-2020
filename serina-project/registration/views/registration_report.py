from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
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
    SubmitNotesForm,
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
):
    """ListView for ModuleRegistrationReport.

    The view support user filters on student, module, degree, course and
    status.
    """

    model = ModuleRegistrationReport
    context_object_name = "modules_rrs"
    template_name = "registration/registration_report/module_rr_listview.html"

    def get_queryset(self):
        """Apply filters if submitted by user."""

        # GET variables

        search_student = self.request.GET.get('q_student')
        search_module = self.request.GET.get('q_module')
        search_degree = self.request.GET.get('q_degree')
        search_course = self.request.GET.get('q_course')
        search_status = self.request.GET.get('q_status')

        # Main query

        query_result = ModuleRegistrationReport.objects.all()

        # Foreign key conditions

        if search_student:
            query_result = query_result.filter(
                student_rr__created_by__pk=search_student,
            )

        if search_module:
            query_result = query_result.filter(
                module__pk=search_module,
            )

        if search_degree:
            query_result = query_result.filter(
                degree_rr__degree__pk=search_degree,
            )

        if search_course:
            query_result = query_result.filter(
                course__pk=search_course,
            )

        if search_status:
            query_result = query_result.filter(
                status=search_status,
            )

        # Query result

        return query_result.order_by("status")

    def get_context_data(self, **kwargs):
        """Add search values to context."""

        context = super().get_context_data(**kwargs)

        # GET variables for search filters

        context['q_student'] = self.request.GET.get('q_student')
        context['q_module'] = self.request.GET.get('q_module')
        context['q_degree'] = self.request.GET.get('q_degree')
        context['q_course'] = self.request.GET.get('q_course')
        context['q_status'] = self.request.GET.get('q_status')

        # Search values

        context['s_students'] = User.objects.filter(
            groups__name="Student",
            student_rr__isnull=False,
        )
        context['s_modules'] = models.Module.objects.all()
        context['s_degrees'] = models.Degree.objects.all()
        context['s_courses'] = models.Course.objects.all()
        context['s_statuses'] = ModuleRegistrationReport.STATUS

        return context


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
            context["form_notes"] = SubmitNotesForm

            if self.get_object().final_score:
                context['final_score_value'] = self.get_object().final_score

            if self.get_object().notes:
                context['notes_value'] = self.get_object().notes

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
