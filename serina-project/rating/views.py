from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic
from django.urls import reverse_lazy

from .forms import StudentRatingForm
from .models import StudentRating
from registration.utils import (
    messages as messages_utils,
    mixins as mixins_utils
)


class StudentRatingListView(LoginRequiredMixin, generic.ListView,):  # TODO: Debug view
    """ListView for StudentRating"""

    model = StudentRating
    context_object_name = "ratings"
    template_name = "rating/rating_listview.html"
    paginate_by = 10


class StudentRatingDetailView(LoginRequiredMixin, generic.DetailView,):  # TODO: Debug view
    """DetailView for StudentRating"""

    model = StudentRating
    context_object_name = "rating"
    template_name = "rating/rating_detailview.html"


class StudentRatingCreateView(
    LoginRequiredMixin,
    mixins_utils.StudentOnlyMixin,
    generic.CreateView,
    mixins_utils.AutofillCreatedByRequestUser,
):  # TODO: Debug view
    """CreateView for StudentRating"""

    model = StudentRating
    form_class = StudentRatingForm
    template_name = "rating/rating_createview.html"


class StudentRatingUpdateView(
    LoginRequiredMixin,
    mixins_utils.SelfStudentManagerAdministratorOnlyMixin,
    generic.UpdateView,
    mixins_utils.AutofillCreatedByRequestUser,
):  # TODO: Debug view
    """UpdateView for StudentRating"""

    model = StudentRating
    form_class = StudentRatingForm
    context_object_name = "rating"
    template_name = "rating/rating_updateview.html"


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
