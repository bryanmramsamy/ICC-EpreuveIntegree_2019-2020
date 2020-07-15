from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import CustomAuthenticationForm


class CustomLoginView(LoginView):
    """Customized Login View."""

    template_name = "registration/login.html"
    authentication_form = CustomAuthenticationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.GET.get('logout') is not None:
            messages.success(
                self.request,
                "You have been logged out successfully"
            )

        return context


def customLogout(request):
    """Logout redirection"""

    logout(request)
    messages.success(request, "You have been logged out successfully")
    return redirect('{}?logout=True'.format(reverse('login')))
