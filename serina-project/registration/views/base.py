from django.shortcuts import render


def home(request):  # TODO: Debug view
    """Homepage render."""

    return render(request, "registration/general/home.html", {})


def home_old(request):  # TODO: Debug view
    """Old omepage render."""

    return render(request, "registration/general/home_old.html", {})