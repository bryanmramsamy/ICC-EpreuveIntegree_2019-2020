import random

from django.utils import translation
from django.shortcuts import render

from management.models import Degree, Module
from rating.models import StudentRating


def home(request):
    """Homepage render.

    Add 3 random Degree and Module instances to the context."""

    # user_language = "fr"
    # translation.activate(user_language)
    # request.session[translation.LANGUAGE_SESSION_KEY] = user_language

    degrees = Degree.objects.order_by("?")[:3]
    modules = Module.objects.order_by("?")[:3]
    ratings = StudentRating.objects.order_by("?")[:4]

    return render(
        request,
        "registration/general/home.html",
        locals(),
    )


def home_old(request):  # TODO: Debug view
    """Old omepage render."""

    return render(request, "registration/general/home_old.html", {})