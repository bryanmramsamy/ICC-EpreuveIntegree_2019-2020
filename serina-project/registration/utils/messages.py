from django.conf import settings
from django.contrib import messages
from django.utils.translation import ugettext as _


# Authentication

def user_is_authenticated(request):
    """Check if a user is authenticated and send message if this is true."""

    is_authenticated = False
    if request.user.is_authenticated:
        is_authenticated = True
        messages.warning(
            request,
            _("You are already signed in. "
              "Please sign out to use a different account.")
        )
    return is_authenticated


# Access control

def permission_denied(request):
    """Warns the user (s)he tried to perform an action without having the
    right permissions."""

    messages.error(
        request,
        _("You are not allowed to perform this action. Please contact the "
          "support team ({}) for more information."
          .format(settings.CONTACT_MAILS["support"]))
    )


# StudentRegistrationReport

def student_rr_created(request):
    """Inform the user that his/her StudentRegistrationReport has correctly
    been saved and that the user was promoted to the 'Student'-group."""

    messages.success(
        request,
        _("Your registration report has successfully been submitted. You now "
          "have the 'Student' status and can subscrib to any degree or any "
          "module wanted.")
    )


# ModuleResgitrationReport Validation


def module_rr_approved(request):
    """Inform the user that the ModuleRegistrationReport object has
    successfully been approved."""

    messages.success(
        request,
        _("The module's registration has been approved. A notification mail "
          "has been sent to the student.")
    )


def module_rr_already_approved(request):
    """Warns the user that the ModuleRegistrationReport object (s)he wants to
    approve has already been approved."""

    messages.warning(
        request,
        _("This module registration request has already been approved.")
    )
