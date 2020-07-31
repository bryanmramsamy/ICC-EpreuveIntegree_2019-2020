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
    PasswordResetView,
)
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.translation import ugettext as _

from .forms import (
    CustomAuthenticationForm,
    CustomPasswordChangeForm,
    CustomPasswordResetForm,
    RegistrationForm,
)
from .utils import messages as messages_utils
from .utils import groups as groups_utils
from .utils import signals as signals_utils
from .utils import users as users_utils


def register(request):
    """Register function which creates an new User and a new linked
    UserProfile."""

    if (messages_utils.user_is_authenticated(request)
            or messages_utils.user_is_disabled(request)):
        return redirect('home')
    else:
        form = RegistrationForm(request.POST or None)

        if form.is_valid():

            # Clean data

            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]

            # Generate username (unique registration number)

            if User.objects.count() == 0:
                latest_user_pk = 1
            else:
                latest_user_pk = User.objects.latest('pk').pk

            date_today = date.today()

            username = users_utils.username_generator(
                latest_user_pk+1,
                date_today,
            )

            # User creation

            user = User.objects.create(
                username=username,
                email=email,
                first_name=first_name.title(),
                last_name=last_name.title(),
            )

            user.set_password(form.cleaned_data["password"])
            groups_utils.promote_to_guest(user)
            user.save()

            # Authentication

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

    template_name = "registration/passwd_change.html"
    form_class = CustomPasswordChangeForm


class CustomPasswordResetView(PasswordResetView):
    """Customized PasswordResetView."""

    template_name = "registration/passwd_reset.html"
    form_class = CustomPasswordResetForm
    # email_template_name = "registration/password_reset_email.html"
    # subject_template_name = "registration/password_reset_subject.txt"
    success_url = reverse_lazy("password_reset_done")
    # from_email = "Serina@SerinaProject.com"  # DEFAULT_FROM_EMAIL = "Serina@SerinaProject.com"


class CustomPasswordResetDoneView(PasswordResetDoneView):
    """Customized PasswordResetDoneView."""

    template_name = "registration/passwd_reset_done.html"


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """ Curtomized PasswordResetConfirmView."""

    template_name = "registration/passwd_reset_confirm.html"
    # form_class = CustomSetPasswordForm
    success_url = reverse_lazy("password_reset_complete")


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    """Customized PasswordResetCompleteView."""

    template_name = "registration/passwd_reset_complete.html"


def post_password_change_logout(request):
    """Log the user out after his/her password has been changed or reset.

    Display a message to the user too.
    """

    messages.success(
        request,
        _("Your password has been changed. You must log yourself in again with"
          " the new password.")
    )
    logout(request)

    return redirect('home')
