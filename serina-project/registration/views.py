from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import (
    LoginView,
    PasswordChangeView,
    PasswordChangeDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
    PasswordResetDoneView,
    PasswordResetView
)
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import ugettext as _

from .forms import (
    CustomAuthenticationForm,
    CustomPasswordChangeForm
)


class CustomLoginView(LoginView):
    """Customized LoginView."""

    template_name = "registration/login.html"
    authentication_form = CustomAuthenticationForm


def customLogout(request):
    """Logout redirection."""

    logout(request)
    messages.success(request, _("You have been logged out successfully"))
    return redirect(reverse('login'))


class CustomPasswordChangeView(PasswordChangeView):
    """Customized PasswordChangeView."""

    template_name = "registration/password_change.html"
    # success_url = reverse('password_change_done')
    form_class = CustomPasswordChangeForm


def customPasswordChangeDone(request):
    """Password Change Done redirection to login.

    The user must login again after a password change.
    """

    messages.success(
        request,
        _("Your password has been changed. You must log yourself in again.")
    )
    return redirect(reverse('password_change'))


class CustomPasswordResetViews(PasswordResetView):
    """Customized PasswordResetView."""

    template_name = "registration/password_reset.html"
    # form_class = CustomPasswordChangeForm
    # email_template_name = "registration/password_reset_email.html"
    # subject_template_name = "registration/password_reset_subject.txt"
    success_url = "password_reset_done"
    # from_email = "Serina@SerinaProject.com"  # DEFAULT_FROM_EMAIL = "Serina@SerinaProject.com"


class CustomPasswordResetDoneView(PasswordResetDoneView):
    """Customized PasswordResetDoneView."""

    template_name = "registration/password_reset_done.html"


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """ Curtomized PasswordResetConfirmView."""

    template_name = "registration/password_reset_confirm.html"
    post_reset_login = True
    # form_class = CustomSetPasswordForm
    success_url = "password_reset_complete"


class CurtomPasswordResetCompleteView(PasswordResetCompleteView):
    """Customized PasswordResetCompleteView."""

    template_name = "registration/password_reset_complete.html"
