from datetime import date

from django.conf import settings
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
from .utilities import groups_utils, signals, users_utils


def register(request):
    """Register function which creates an new User and a new linked
    UserProfile."""

    if request.user.is_authenticated:
        messages.warning(
            request,
            _("You are already signed in. "
              "Please sign out to use a different account.")
        )
        return redirect('home')
    elif not request.user.is_anonymous and not request.user.is_active:
        messages.error(
            request,
            _("Your account has been disabled. Contact the management team at "
              "this address ({}) to get more information.".format(
                  settings.MAIL_MANAGEMENT
                  ))
        )
        return redirect('home')
    else:
        form = RegistrationForm(request.POST or None)

        if form.is_valid():
            username = "{}.{}".format(
                form.cleaned_data["first_name"],
                form.cleaned_data["last_name"]
            )
            password = form.cleaned_data["password"]
            email = form.cleaned_data["email"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]

            latestUserPk = User.objects.latest('pk').pk
            dateToday = date.today()

            user = User.objects.create(
                username=users_utils.username_generator(
                    latestUserPk+1,
                    dateToday
                ),
                password=password,
                email=email,
                first_name=first_name.title(),
                last_name=last_name.title()
            )

            groups_utils.promote_to_professor(user)
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

    # TODO: Add message when user was already autheticated

    # def get_context_data(self, **kwargs):
    #     context = super(CustomLoginView, self).get_context_data(**kwargs)
    #     messages.error(
    #         self.request,
    #         _("You are already signed in. "
    #           "Please sign out to use a different account.")
    #     )
    #     return context


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
