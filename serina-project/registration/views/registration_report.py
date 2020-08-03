from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, ListView

from ..forms import (
    ModuleRegistrationReportCreateFrom,
    StudentRegistrationReportCreateFrom,
)
from ..models import (
    ModuleRegistrationReport,
    StudentRegistrationReport,
)
from ..utils.mixins import (
    AutofillCreatedByRequestUser,
    ManagerAdministratorOnlyMixin,
)


# StudentRegistrationReport

class StudentRegistrationReportListView(
    LoginRequiredMixin,
    ManagerAdministratorOnlyMixin,
    ListView
):  # TODO: Debug view
    """CreateView for Modules."""

    model = StudentRegistrationReport
    context_object_name = "student_rrs"
    template_name = "registration/registration_report/student_rr_listview." \
                    "html"


class StudentRegistrationReportDetailView(
    LoginRequiredMixin,
    ManagerAdministratorOnlyMixin,
    DetailView
):  # TODO: Debug view
    """CreateView for Modules."""

    # TODO: Restrict access to student who made student_rr
    model = StudentRegistrationReport
    context_object_name = "student_rr"
    template_name = "registration/registration_report/student_rr_detailview." \
                    "html"


class StudentRegistrationReportCreateView(
    LoginRequiredMixin,
    CreateView,
    AutofillCreatedByRequestUser
):  # TODO: Debug view
    """CreateView for StudentRegistrationReport with
    StudentRegistrationReportCreateFrom."""

    # TODO: Restrict access to Guest, not student
    # TODO: The user guest becomes a student when his student_rr has been submitted
    # TODO: Student can not create new student_rr
    model = StudentRegistrationReport
    form_class = StudentRegistrationReportCreateFrom
    template_name = "registration/registration_report/student_rr_createview." \
                    "html"


# ModuleRegistrationReport

class ModuleRegistrationReportCreateView(
    LoginRequiredMixin,
    CreateView,
    AutofillCreatedByRequestUser
):  # TODO: Debug view
    """CreateView for ModuleRegistrationReport with
    ModuleRegistrationReportCreateFrom."""

    #TODO: Restrict access to student (because a student is a user whom submitted his student_rr)
    model = ModuleRegistrationReport
    form_class = ModuleRegistrationReportCreateFrom
    template_name = "registration/registration_report/module_rr_createview." \
                    "html"
