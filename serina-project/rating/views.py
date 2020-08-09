from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import CreateView

from .forms import StudentRatingForm
from .models import StudentRating
from registration.utils import mixins as mixins_utils


class StudentRatingCreateView(
    LoginRequiredMixin,
    # mixins_utils.StudentOnlyMixin,  # TODO: Disabled for debug purposes
    CreateView,
    mixins_utils.AutofillCreatedByRequestUser,
):  # TODO: Debug view
    """CreateView for Rating."""

    model = StudentRating
    form_class = StudentRatingForm
    template_name = "rating/rating_createview.html"
