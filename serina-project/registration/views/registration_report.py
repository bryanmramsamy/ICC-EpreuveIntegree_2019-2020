from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, ListView

from ..forms import StudentRegistrationReportCreateFrom
from ..models import StudentRegistrationReport
from ..utils.mixins import (
    AutofillCreatedByRequestUser,
    ManagerAdministratorOnlyMixin,
)


class StudentRegistrationReportDetailView(
    LoginRequiredMixin,
    ManagerAdministratorOnlyMixin,
    DetailView
):  # TODO: Debug view
    """CreateView for Modules."""

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

    model = StudentRegistrationReport
    form_class = StudentRegistrationReportCreateFrom
    template_name = "registration/registration_report/student_rr_createview." \
                    "html"
