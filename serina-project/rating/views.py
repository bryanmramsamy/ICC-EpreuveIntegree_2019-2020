from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy

from .forms import StudentRatingForm
from .models import StudentRating
from registration.utils import mixins as mixins_utils


class StudentRatingListView(
    LoginRequiredMixin,
    generic.ListView,
):  # TODO: Debug view
    model = StudentRating
    context_object_name = "rating"
    template_name = "rating/rating_listview.html"
    paginate_by = 10


class StudentRatingDetailView(
    LoginRequiredMixin,
    generic.DetailView,
):  # TODO: Debug view
    model = StudentRating
    context_object_name = "rating"
    template_name = "rating/rating_detailview.html"


class StudentRatingCreateView(
    LoginRequiredMixin,
    mixins_utils.SelfStudentManagerAdministratorOnlyMixin,
    generic.CreateView,
    mixins_utils.AutofillCreatedByRequestUser,
):  # TODO: Debug view
    """CreateView for Rating."""

    model = StudentRating
    form_class = StudentRatingForm
    template_name = "rating/rating_createview.html"


class StudentRatingUpdateView(
    LoginRequiredMixin,
    mixins_utils.SelfStudentManagerAdministratorOnlyMixin,
    generic.UpdateView,
    mixins_utils.AutofillCreatedByRequestUser,
):  # TODO: Debug view
    """CreateView for Rating."""

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
    """CreateView for Rating."""

    model = StudentRating
    form_class = StudentRatingForm
    template_name = "rating/rating_deleteview.html"
    success_url = reverse_lazy('module_listview')