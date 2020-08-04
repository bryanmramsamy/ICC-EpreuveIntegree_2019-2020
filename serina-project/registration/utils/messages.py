from django.conf import settings
from django.contrib import messages
from django.utils.translation import ugettext as _


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


# TODO: Check if function usefull
# def user_is_anonymous(request):
#     """Check if a user is anonymous (not authenticated yet) and send message
#     if this is true."""

#     is_anonymous = False
#     if request.user.is_anonymous:
#         is_anonymous = True
#         messages.warning(
#             request,
#             _("You are not signed in yet. If you don't have an account, "
#               "<a href='{}'>register now</a>.".format(reverse('register')))
#         )
#     return is_anonymous


# TODO: Check if function usefull
# def user_is_disabled(request):
#     """Check if a user's account has been disabled and send message if this is
#     true."""

#     is_disabled = False
#     if not request.user.is_anonymous and not request.user.is_active:
#         is_disabled = True
#         messages.error(
#             request,
#             _("Your account has been disabled. Contact the support team ({}) "
#               "to get more information."
#               .format(settings.CONTACT_MAILS["support"]))
#         )
#     return is_disabled


# TODO: Not tested yet
def username_changed(request, old_username, new_username):
    """Warns the user that his/her username has been changed."""

    messages.warning(
        request,
        _("Your username has been changed and is now {} (was {})."
          .format(new_username, old_username))
    )


def student_rr_created(request):
    """Inform the user that his/her StudentRegistrationReport has correctly
    been saved and that the user was promoted to the 'Student'-group."""

    messages.success(
        request,
        _("Your registration report has successfully been submitted. You now "
          "have the 'Student' status and can subscrib to any degree or any "
          "module wanted.")
    )
