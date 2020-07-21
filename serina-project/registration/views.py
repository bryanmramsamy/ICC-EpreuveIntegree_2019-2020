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


def register(request):
    """Register function which creates an new User and a new linked
    UserProfile."""

    # TODO: Check if user is active and already authenticated

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

        user = User.objects.create(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name
        )

        UserProfile.objects.create(
            user=user,
            birthday=form.cleaned_data["birthday"],
            nationality=form.cleaned_data["nationality"],
            address=form.cleaned_data["address"],
            postalCode=form.cleaned_data["postalCode"],
            postalLocality=form.cleaned_data["postalLocality"]
        )

        # user = authenticate(username=username, password=password)
        # NOTE: Not needed because the user is already defined in line 44
        login(request, user)

        return redirect('home')
    else:
        return render(request, "registration/register.html", locals())


def inscription(request):
    """Register a new user"""

    user_form = UserForm(request.POST or None)
    profil_form = ProfilForm(request.POST or None)

    if user_form.is_valid() and profil_form.is_valid():
        user = user_form.save()
        profil = profil_form.save(commit=False)
        # signal to create profile has been deactivated because profil.pk was used twice

        profil.user = user
        profil.save()

        return redirect('home')
    else:
        return render(request, 'blog/signup.html', locals())



class CustomLoginView(LoginView):
    """Customized LoginView."""

    template_name = "registration/login.html"
    authentication_form = CustomAuthenticationForm


def customLogout(request):
    """Logout redirection."""

    logout(request)
    messages.success(request, _("You have been logged out successfully"))
    return redirect('login')


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
