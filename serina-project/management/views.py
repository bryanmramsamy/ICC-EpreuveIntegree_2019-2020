from django.shortcuts import render


def home(request):
    """Homepage render."""

    return render(request, "management/home.html", {})
