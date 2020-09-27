import random

from django.utils import translation
from django.shortcuts import render

from management.models import Degree, Module
from rating.models import StudentRating


def home(request):
    """Homepage render.

    Add 3 random Degree and Module instances to the context."""

    degrees = Degree.objects.order_by("?")[:3]
    modules = Module.objects.order_by("?")[:3]
    ratings = StudentRating.objects.order_by("?")[:4]

    return render(
        request,
        "registration/general/home.html",
        locals(),
    )


def terms_and_conditions(request):
    """Render the 'Terms and conditions' page."""

    return render(request, "registration/general/terms_and_conditions.html")


def privacy_policy(request):
    """Render the 'Pricacy Policy' page."""

    return render(request, "registration/general/privacy_policy.html")


def cookies_policy(request):
    """Render the 'Cookies policy' page."""

    return render(request, "registration/general/cookies_policy.html")
