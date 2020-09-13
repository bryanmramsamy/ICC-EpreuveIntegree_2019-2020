from datetime import date

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
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

from ..forms import (
    CustomAuthenticationForm,
    CustomPasswordChangeForm,
    CustomPasswordResetForm,
    RegistrationForm,
)
from ..utils import (
    groups as groups_utils,
    decorators as decorators_utils,
    messages as messages_utils,
    users as users_utils,
)


def register(request):
    """Register function which creates an new User and a new linked
    UserProfile."""

    support_mail = settings.CONTACT_MAILS["support"]

    if messages_utils.user_is_authenticated(request):
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
                latest_user_pk = 0
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
            return render(
                request,
                "registration/authentication/register.html",
                locals(),
            )


@decorators_utils.guests_only
def pursue_registration(request):
    """Render a view giving the opportunity to the user to pursue his/her
    registration.

    If the user doesn't pursue the registration (s)he will hold the
    'Registered-Guest' role. Otherwise the user will switch to the 'Student'
    role if the registration is completed.
    """

    return render(request, "registration/authentication/pursue_register.html")


class CustomLoginView(LoginView):
    """Customized LoginView."""

    template_name = "registration/authentication/login.html"
    authentication_form = CustomAuthenticationForm
    redirect_authenticated_user = True


@login_required
def customLogout(request):
    """Logout redirection."""

    logout(request)
    messages_utils.user_logged_out(request)
    return redirect('home')


class CustomPasswordChangeView(PasswordChangeView):
    """Customized PasswordChangeView."""

    template_name = "registration/authentication/passwd_change.html"
    form_class = CustomPasswordChangeForm


class CustomPasswordResetView(PasswordResetView):
    """Customized PasswordResetView."""

    # TODO: Use custom template mail + change subject and from_mail
    template_name = "registration/authentication/passwd_reset.html"
    form_class = CustomPasswordResetForm
    # email_template_name = "registration/authentication/password_reset_email.html"
    # subject_template_name = "registration/authentication/password_reset_subject.txt"
    success_url = reverse_lazy("password_reset_done")
    # from_email = "Serina@SerinaProject.com"  # DEFAULT_FROM_EMAIL = "Serina@SerinaProject.com"


class CustomPasswordResetDoneView(PasswordResetDoneView):
    """Customized PasswordResetDoneView."""

    template_name = "registration/authentication/passwd_reset_done.html"


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """ Curtomized PasswordResetConfirmView."""

    template_name = "registration/authentication/passwd_reset_confirm.html"
    # form_class = CustomSetPasswordForm
    success_url = reverse_lazy("password_reset_complete")


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    """Customized PasswordResetCompleteView."""

    template_name = "registration/authentication/passwd_reset_complete.html"


def post_password_change_logout(request):
    """Log the user out after his/her password has been changed or reset.

    Display a message to the user too.
    """

    messages_utils.password_changed(request)
    logout(request)

    return redirect('home')
