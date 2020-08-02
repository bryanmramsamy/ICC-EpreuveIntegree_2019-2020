from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.utils.translation import gettext as _

from . import groups as groups_utils


class BackOfficeUsersOnlyMixin(UserPassesTestMixin):
    """Restrict view access to Back-Office users."""

    def test_func(self):
        """Check if the user is a Back-Office user."""

        return groups_utils.is_back_office_user(self.request.user)

    def handle_no_permission(self):
        """Send an error message and redirect the home page."""

        messages.error(
            self.request,
            _("You are not allowed to access the requested page or perform the"
              " attempted action. Please contact the support team ({}) for "
              "more information.".format(settings.CONTACT_MAILS["support"]))
        )
        return redirect('home')


class ManagerAdministratorOnlyMixin(BackOfficeUsersOnlyMixin):
    """Restrict view access to 'Manager'-group members and
    'Administrator'-group members."""

    def test_func(self):
        """Check if the user is a Manager or an Administrator."""

        return groups_utils.is_manager_or_administrator(self.request.user)
