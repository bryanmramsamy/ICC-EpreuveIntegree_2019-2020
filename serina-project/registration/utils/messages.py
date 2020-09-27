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


# User's group promotion

def promote_to_group(request, user, group):
    """Inform that a user successfully has been promoted as guest."""

    messages.success(
        request,
        _("{} ({}) has successfully been promoted to the {} group."
          .format(user.get_full_name(), user.username, group.name))
    )


def cannot_promote_to_student_student_rr_missing(request, user):
    """Warn that a user wan't promoted as student bacause the user hasn't a
    Student Registration Report yet.."""

    messages.error(
        request,
        _(
            "{} ({}) can not be promoted to the Student group. The user "
            "doesn't has his/her own Student Registration Report which is "
            "mandatory for joining this group."
            .format(user.get_full_name(), user.username)
        )
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


def module_rr_denied(request):
    """Inform the user that the ModuleRegistrationReport object has
    successfully been denied."""

    messages.success(
        request,
        _("The module's registration has been denied. A notification mail has "
          "been sent to the student.")
    )


def module_rr_already_denied(request):
    """Warns the user that the ModuleRegistrationReport object (s)he wants to
    approve has already been denied."""

    messages.warning(
        request,
        _("This module registration request has already been denied.")
    )


# ModuleResgitrationReport Final Score Submission

def module_rr_final_score_submitted(request):
    """Inform the user that the final score has been successfully applied to
    the module registration request."""

    messages.success(
        request,
        _("The module score has been added and has now been completed.")
    )


def module_rr_already_completed(request):
    """Warns the user that the module on which (s)he tries to submit a score
    was already completed."""

    messages.error(
        request,
        _("This module registration request is already completed. The final "
          "score cannot be changed anymore without an adminitrator ({})"
          .format(settings.CONTACT_MAILS["administrators"]))
    )


def module_rr_final_score_while_denied(request):
    """Warns the user that the module on which (s)he tries to submit a score
    has been denied."""

    messages.error(
        request,
        _("This module registration request has been denied and can therefore "
          "not been rated.")
    )


def module_rr_not_payed(request):
    """Warns the user that the module on which (s)he tries to submit a score
    has not been payed yet."""

    messages.warning(
        request,
        _("This module registration request has not been payed by the student "
          "yet. The final score was saved anyway but the module cannot be "
          "coonsidered as completed as long as the payment wasn't done.")
    )


def module_rr_notes_updated(request):
    """Informs the user that the notes from the Module Registration Request has
    correctly been updated."""

    messages.success(
        request,
        _("The notes for this module report has correctly been updated.")
    )


# ModuleRegistrationReport payment

def module_payment_succeeded(request):
    """Inform the user the payment has been successfully completed."""

    messages.success(
        request,
        _("The module has been successfully payed.")
    )


def module_payment_failed(request):
    """Warn the user the payment has failed."""

    messages.error(
        request,
        _("The module payment has unexpectedly been aborted.")
    )


def module_not_payable(request):
    """Warns the user the module request cannot be payed because it has not an
    'APPROVED' status."""

    messages.error(
        request,
        _("This module registration request cannot be payed. It has either "
          "not been approved, is already payed, completed or exempted.")
    )


# User (de)activation

def user_activated(request):
    """Warns the manager/administrator that the selected user's account has
    been activated."""

    messages.success(
        request,
        _(
            "The selected user's account has been successfully re-enabled. "
            "It can be disabled again without cuasing any data loss."
        )
    )


def user_deactivated(request):
    """Warns the manager/administrator that the selected user's account has
    been deactivated."""

    messages.success(
        request,
        _(
            "The selected user's account has been successfully disabled. All "
            "his/her is still saved in the database and the account can be "
            "reactivated anytime."
        )
    )
