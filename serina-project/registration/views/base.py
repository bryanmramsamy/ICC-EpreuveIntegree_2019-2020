from django.shortcuts import render


def home(request):  # TODO: Debug view
    """Homepage render."""

    return render(request, "registration/general/home.html", {})
