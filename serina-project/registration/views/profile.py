from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.views.generic import DetailView, FormView
from django.urls import reverse

from ..forms import StudentProfileUpdateForm, UserProfileUpdateForm
from ..models import(
    DegreeRegistrationReport,
    ModuleRegistrationReport,
    StudentRegistrationReport,
)
from ..utils.groups import is_student, main_group_i18n
from ..utils import mixins as mixins_utils
from management.models import Course


class UserProfileDetailView(
    LoginRequiredMixin,
    mixins_utils.ManagerAdministratorOnlyMixin,
    DetailView,
):
    """User's profile view with all his/her related data.

    If the user is a student, (s)he should have a related StudentRegistration-
    Report. Fetch the StudentRegistrationReport data with the related
    DegreeRegistrationReports and ModuleRegistrationReports.
    """

    model = User
    context_object_name = "userprofile"
    template_name = "registration/userprofile/userprofile_detailview.html"

    def test_func(self):
        """Check if the user is not consulting anothers user's profile or is a
        Manager or an Administrator."""

        is_self_user = self.get_object().pk == self.request.user.pk

        return super(UserProfileDetailView, self).test_func() \
            or is_self_user

    def get_context_data(self, **kwargs):
        """Add more data related to user to the context. The user's profile
        page is used as overview the user's activity too.

        Add the user's main group name to the context.
        If the user is a registered student, his/her StudentRegistrationReport
        and its related DegreeRegistrationReports, related
        ModuleRegistrationReports and the Courses the student is subscribed on
        are added to the context too.
        """

        context = super(UserProfileDetailView, self).get_context_data(**kwargs)
        context["is_self_user"] = self.get_object().pk == self.request.user.pk
        context["main_group"] = main_group_i18n(self.get_object())

        if is_student(self.get_object()):
            context["student_rr"] = StudentRegistrationReport.objects.get(
                created_by=self.get_object()
            )

            # Module Registration Reports

            context["modules_rrs"] = ModuleRegistrationReport.objects.filter(
                student_rr=context["student_rr"],
            )
            context["nb_approved_modules_rrs"] = \
                len([x for x in context["modules_rrs"] if x.approved])
            context["nb_exempted_modules_rrs"] = context["modules_rrs"].filter(
                status="EXEMPTED",
            ).count()
            context["nb_denied_modules_rrs"] = context["modules_rrs"].filter(
                status="DENIED",
            ).count()
            context["nb_payed_modules_rrs"] = \
                len([x for x in context["modules_rrs"] if x.payed])
            context["nb_succeeded_modules_rrs"] = \
                len([x for x in context["modules_rrs"] if x.succeeded])
            context["nb_payements_pending_modules_rrs"] = \
                context["nb_approved_modules_rrs"] \
                - context["nb_payed_modules_rrs"]

            # Degree Registration Reports

            context["degrees_rrs"] = DegreeRegistrationReport.objects.filter(
                student_rr=context["student_rr"],
            )
            context["nb_partially_approved_degrees_rrs"] = \
                len([x for x in context["degrees_rrs"]
                    if x.partially_approved])
            context["nb_fully_approved_degrees_rrs"] = \
                len([x for x in context["degrees_rrs"] if x.fully_approved]) \
                - context["nb_partially_approved_degrees_rrs"]
            context["nb_partially_payed_degrees_rrs"] = \
                len([x for x in context["degrees_rrs"] if x.partially_payed])
            context["nb_fully_payed_degrees_rrs"] = \
                len([x for x in context["degrees_rrs"] if x.fully_payed]) \
                - context["nb_partially_payed_degrees_rrs"]
            context["nb_payements_pending_degrees_rrs"] = \
                context["nb_fully_approved_degrees_rrs"] \
                - context["nb_fully_payed_degrees_rrs"]
            context["nb_graduated_degrees_rrs"] = \
                len([x for x in context["degrees_rrs"] if x.student_graduated])

            # Courses

            context["courses"] = []  # TODO: Find a way to express this in queryset
            for module_rr in context["modules_rrs"]:
                if module_rr.course:
                    context["courses"].append(module_rr.course)

        return context


class UserProfileUpdateView(LoginRequiredMixin, FormView):
    """User's profile UpdateView.

    If the user is a student, (s)he can also change the changeable fields of
    his/het StudentRegistrationReport: 'nationality', 'address',
    'additional_address', 'postal_code' and 'postal_locality'.
    """

    template_name = "registration/userprofile/userprofile_updateview.html"

    def get_form_class(self):
        """Return the StudentProfileUpdateForm if the user is a registered
        student. Otherwise, return the standard UserProfileUpdateForm."""

        if is_student(self.request.user):
            form_class = StudentProfileUpdateForm
        else:
            form_class = UserProfileUpdateForm

        return form_class

    def get_initial(self):
        """Returns the initial data to use for forms on this view."""

        initial = super().get_initial()

        user = User.objects.get(pk=self.request.user.pk)

        initial['first_name'] = user.first_name
        initial['last_name'] = user.last_name
        initial['email'] = user.email

        if is_student(self.request.user):
            student_rr = StudentRegistrationReport.objects.get(created_by=user)

            initial['nationality'] = student_rr.nationality
            initial['address'] = student_rr.address
            initial['additional_address'] = student_rr.additional_address
            initial['postal_code'] = student_rr.postal_code
            initial['postal_locality'] = student_rr.postal_locality

        return initial

    def form_valid(self, form):
        """If the form is valid, save the updated user profile data. Update the
        StudentRegistrationReport as well if the user is a registered student.
        """

        user = User.objects.get(pk=self.request.user.pk)

        user.first_name = form.cleaned_data["first_name"]
        user.last_name = form.cleaned_data["last_name"]
        user.email = form.cleaned_data["email"]

        user.save()

        if is_student(self.request.user):

            student_rr = StudentRegistrationReport.objects.get(created_by=user)

            student_rr.nationality = form.cleaned_data["nationality"]
            student_rr.address = form.cleaned_data["address"]
            student_rr.additional_address = form.cleaned_data[
                "additional_address"
            ]
            student_rr.postal_code = form.cleaned_data["postal_code"]
            student_rr.postal_locality = form.cleaned_data["postal_locality"]

            student_rr.save()

        return super().form_valid(form)

    def get_success_url(self):
        """Redirect to the user's profile if the submitted form was valid and
        the profile updated."""

        return reverse("userprofile_detailview",
                       kwargs={"pk": self.request.user.pk})
