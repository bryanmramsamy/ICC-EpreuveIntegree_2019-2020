from django.contrib.auth.models import User
from django.db.models import Q
from django.views.generic import DetailView, FormView

from ..models import(
    ModuleRegistrationReport,
    StudentRegistrationReport,
)
from ..utils.groups import main_group_i18n
from management.models import Course


class UserProfileDetailView(DetailView):
    """User's profile view with all his/her related data."""

    model = User
    context_object_name = "user"
    template_name = "registration/userprofile/userprofile_detailview.html"

    def get_context_data(self, **kwargs):
        """Add the folowing data to the context:

        * The name of the user's main group.
        * The StudentRegistrationReport
        * The related DegreeRegistrationReports and ModuleRegistrationReports
        * The related courses
        """

        context = super(UserProfileDetailView, self).get_context_data(**kwargs)
        context["main_group"] = main_group_i18n(self.request.user)
        context["student_rr"] = StudentRegistrationReport.objects.get(
            created_by=self.request.user
        )
        context["modules_rrs"] = ModuleRegistrationReport.objects.filter(
            student_rr=context["student_rr"]
        )
        context["courses"] = []  # TODO: Find a way to express this in queryset
        for module_rr in context["modules_rrs"]:
            context["courses"].append(module_rr.course)

        return context


class UserProfileUpdateView(FormView):
    pass
