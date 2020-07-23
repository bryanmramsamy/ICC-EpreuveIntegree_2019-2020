from datetime import date

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
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
    CustomPasswordChangeForm,
    CustomPasswordResetForm,
    RegistrationForm
)
from .models import UserProfile
from .utilities import messages_utils, groups_utils, signals_utils, users_utils


def register(request):
    """Register function which creates an new User and a new linked
    UserProfile."""

    if (messages_utils.user_is_authenticated(request)
        or messages_utils.user_is_disabled(request)):
        return redirect('home')
    else:
        form = RegistrationForm(request.POST or None)

        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]

            latestUserPk = User.objects.latest('pk').pk
            dateToday = date.today()

            user = User.objects.create(
                username=users_utils.username_generator(
                    latestUserPk+1,
                    dateToday
                ),
                email=email,
                first_name=first_name.title(),
                last_name=last_name.title()
            )

            user.set_password(form.cleaned_data["password"])
            groups_utils.promote_to_guest(user)
            user.save()

            UserProfile.objects.create(
                user=user,
                birthday=form.cleaned_data["birthday"],
                nationality=form.cleaned_data["nationality"],
                address=form.cleaned_data["address"],
                postalCode=form.cleaned_data["postalCode"],
                postalLocality=form.cleaned_data["postalLocality"]
            )

            login(request, user)

            return redirect('home')
        else:
            return render(request, "registration/register.html", locals())


class CustomLoginView(LoginView):
    """Customized LoginView."""

    template_name = "registration/login.html"
    authentication_form = CustomAuthenticationForm
    redirect_authenticated_user = True


def customLogout(request):
    """Logout redirection."""

    logout(request)
    messages.success(request, _("You have been logged out successfully"))
    return redirect('home')


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
    return redirect('home')


class CustomPasswordResetView(PasswordResetView):
    """Customized PasswordResetView."""

    template_name = "registration/password_reset.html"
    form_class = CustomPasswordResetForm
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


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    """Customized PasswordResetCompleteView."""

    template_name = "registration/password_reset_complete.html"
