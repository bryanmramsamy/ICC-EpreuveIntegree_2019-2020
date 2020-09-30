from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic
from django.urls import reverse, reverse_lazy

from .forms import StudentRatingForm
from .models import StudentRating
from registration.models import Degree, Module
from registration.utils import (
    messages as messages_utils,
    mixins as mixins_utils,
    registration as registration_utils,
)


class StudentRatingListView(
    LoginRequiredMixin,
    mixins_utils.ManagerAdministratorOnlyMixin,
    generic.ListView,
):
    """ListView for StudentRating"""

    model = StudentRating
    context_object_name = "ratings"
    template_name = "rating/rating_listview.html"

    def get_queryset(self):
        """Apply filters if submitted by user."""

        # GET variables

        search_student = self.request.GET.get('q_student')
        search_module = self.request.GET.get('q_module')
        search_degree = self.request.GET.get('q_degree')
        search_rate = self.request.GET.get('q_rate')
        search_is_visible = self.request.GET.get('q_is_visible')

        # Main query

        query_result = StudentRating.objects.all()

        # Filtering

        if search_student:
            query_result = query_result.filter(
                created_by__pk=search_student,
            )

        if search_module:
            query_result = query_result.filter(
                module__pk=search_module,
            )

        if search_degree:
            query_result = query_result.filter(
                degree__pk=search_degree,
            )

        if search_rate:
            query_result = query_result.filter(
                rate=search_rate,
            )

        if search_is_visible:
            query_result = query_result.filter(
                is_visible=search_is_visible,
            )

        # Query result

        return query_result.order_by("date_updated")

    def get_context_data(self, **kwargs):
        """Add search values to context."""

        context = super().get_context_data(**kwargs)

        # GET variables for search filters

        context['q_student'] = self.request.GET.get('q_student')
        context['q_module'] = self.request.GET.get('q_module')
        context['q_degree'] = self.request.GET.get('q_degree')
        context['q_rate'] = self.request.GET.get('q_rate')
        context['q_is_visible'] = self.request.GET.get('q_is_visible')

        # Search values

        context['s_students'] = User.objects.filter(
            groups__name="Student",
            student_rr__isnull=False,
        )
        context['s_modules'] = Module.objects.all()
        context['s_degrees'] = Degree.objects.all()
        context['s_rates'] = [1, 2, 3, 4, 5]

        return context


class StudentRatingCreateView(
    LoginRequiredMixin,
    mixins_utils.StudentOnlyMixin,
    generic.CreateView,
    mixins_utils.AutofillCreatedByRequestUser,
):
    """CreateView for StudentRating"""

    model = StudentRating
    form_class = StudentRatingForm
    template_name = "rating/rating_createview.html"

    def test_func(self):
        """Check if the student succeeded the module/degree and if (s)he didn't
        already left a rating before."""

        if self.kwargs["type"] == "module":

            # Check if student succeeded
            student_succeeded = registration_utils \
                .succeeded_module_rr_already_exists(
                    self.request.user,
                    get_object_or_404(Module, pk=self.kwargs["pk"]),
                )

            # Check if student already left a rate
            no_rate_left = not StudentRating.objects.filter(
                created_by=self.request.user,
                module=get_object_or_404(Module, pk=self.kwargs["pk"]),
            ).exists()

        elif self.kwargs["type"] == "degree":

            # Check if student already left a rate
            student_succeeded = registration_utils \
                .succeeded_degree_rr_already_exists(
                    self.request.user,
                    get_object_or_404(Degree, pk=self.kwargs["pk"]),
                )

            # Check if student already left a rate
            no_rate_left = not StudentRating.objects.filter(
                created_by=self.request.user,
                degree=get_object_or_404(Degree, pk=self.kwargs["pk"]),
            ).exists()

        if not student_succeeded:
            messages_utils.failed_no_rating(self.request)

        elif not no_rate_left:
            messages_utils.already_rated(self.request)

        return super(StudentRatingCreateView, self).test_func() \
            and student_succeeded and no_rate_left

    def get_initial(self):
        """Returns the initial data to use for forms on this view."""

        initial = super().get_initial()
        initial['created_by'] = self.request.user

        if self.kwargs["type"] == "module":
            initial['module'] = get_object_or_404(Module, pk=self.kwargs["pk"])

        elif self.kwargs["type"] == "degree":
            initial['degree'] = get_object_or_404(Degree, pk=self.kwargs["pk"])

        return initial

    def get_context_data(self, **kwargs):
        """Add check variables for template conditions."""

        context = super().get_context_data(**kwargs)

        if self.kwargs["type"] == "module":
            context['module'] = get_object_or_404(Module, pk=self.kwargs["pk"])

        elif self.kwargs["type"] == "degree":
            context['degree'] = get_object_or_404(Degree, pk=self.kwargs["pk"])

        return context


class StudentRatingUpdateView(
    LoginRequiredMixin,
    mixins_utils.SelfStudentManagerAdministratorOnlyMixin,
    generic.UpdateView,
    mixins_utils.AutofillCreatedByRequestUser,
):
    """UpdateView for StudentRating"""

    model = StudentRating
    form_class = StudentRatingForm
    context_object_name = "rating"
    template_name = "rating/rating_updateview.html"

    def get_initial(self):
        """Returns the initial data to use for forms on this view."""

        initial = super().get_initial()
        initial['created_by'] = self.request.user

        if self.get_object().module:
            initial['module'] = self.get_object().module

        elif self.get_object().degree:
            initial['degree'] = self.get_object().degree

        return initial


class StudentRatingDeleteView(
    LoginRequiredMixin,
    mixins_utils.SelfStudentManagerAdministratorOnlyMixin,
    generic.DeleteView,
    mixins_utils.AutofillCreatedByRequestUser,
):
    """DeleteView for StudentRating"""

    model = StudentRating
    form_class = StudentRatingForm
    context_object_name = "rating"
    template_name = "rating/rating_deleteview.html"

    def get_success_url(self):
        """Redirect to module/degree page after deletation."""

        if self.get_object().module:
            redirection = get_object_or_404(Module,
                                            pk=self.get_object().module.pk)

        elif self.get_object().degree:
            redirection = get_object_or_404(Degree,
                                            pk=self.get_object().degree.pk)

        return redirection.get_absolute_url()


def change_visibility(request, pk):
    """Change the visibility of a rating."""

    rating = get_object_or_404(StudentRating, pk=pk)

    if rating.is_visible:
        rating.is_visible = False
        messages_utils.rating_is_invisible(request)

    else:
        rating.is_visible = True
        messages_utils.rating_is_visible(request)

    rating.save()

    if rating.module:
        redirection = rating.module

    else:
        redirection = rating.degree

    return redirect(redirection)
