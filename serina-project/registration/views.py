from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import (
    LoginView,
    PasswordChangeView,
    PasswordChangeDoneView
)
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import ugettext as _

from .forms import (
    CustomAuthenticationForm,
    CustomPasswordChangeForm
)


class CustomLoginView(LoginView):
    """Customized Login View."""

    template_name = "registration/login.html"
    authentication_form = CustomAuthenticationForm


def customLogout(request):
    """Logout redirection"""

    logout(request)
    messages.success(request, _("You have been logged out successfully"))
    return redirect(reverse('login'))


class CustomPasswordChangeView(PasswordChangeView):
    template_name = "registration/password_change.html"
    form_class = CustomPasswordChangeForm
