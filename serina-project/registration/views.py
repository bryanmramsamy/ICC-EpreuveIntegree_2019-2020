from django.contrib.auth.views import LoginView
from django.shortcuts import render

from .forms import CustomAuthenticationForm


class CustomLoginView(LoginView):
    """Customized Login View."""

    template_name = "registration/login.html"
    authentication_form = CustomAuthenticationForm
