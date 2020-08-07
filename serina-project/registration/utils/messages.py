from django.conf import settings
from django.contrib import messages
from django.utils.translation import ugettext as _


# Authentication

def user_logged_out(request):
    """Inform the user that (s)he has successfully been logged out."""

    messages.success(request, _("You have been logged out successfully."))


def password_changed(request):
    """Inform the user his/her password has correctly been changed."""

    messages.success(
        request,
        _("Your password has been changed. You must log yourself in again with"
          " the new password.")
    )


def user_is_authenticated(request):  # TODO: Must be decorator
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


def student_rr_already_created(request, student):
    """Warns the user that a StudentRegistrationReport object as already been
    linked to the selected student."""

    messages.error(
        request,
        _("The student registration file has already been created for your "
          "account: {} ({}). You can still change some information from your "
          "student's profile.".format(
              student.get_full_name(),
              student.username,
          ))
    )


# ModuleResgitrationReport Validation

def module_rr_has_no_course(request, module):
    """Warns the user that the ModuleRegistrationReport object cannot be
    validated because there aren't any course related to the module.

    When a module doesn't have any course related to it, the students cannot be
    assign to the course and so the module itself. An error message is prompt.
    """

    messages.error(
        request,
        _("There is no course available for the requested module: {} ({}). In "
          "order to accept any new registration request, a new course must be "
          "created for this module.".format(module.title, module.reference))
    )


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
