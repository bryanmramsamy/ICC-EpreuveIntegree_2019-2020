from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic
from django.urls import reverse_lazy

from .forms import StudentRatingForm
from .models import StudentRating
from registration.models import Degree, Module
from registration.utils import (
    messages as messages_utils,
    mixins as mixins_utils,
    registration as registration_utils,
)


class StudentRatingListView(LoginRequiredMixin, generic.ListView,):  # TODO: Debug view
    """ListView for StudentRating"""

    model = StudentRating
    context_object_name = "ratings"
    template_name = "rating/rating_listview.html"
    paginate_by = 10


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
):  # TODO: Debug view
    """DeleteView for StudentRating"""

    model = StudentRating
    form_class = StudentRatingForm
    template_name = "rating/rating_deleteview.html"
    success_url = reverse_lazy('module_listview')


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
