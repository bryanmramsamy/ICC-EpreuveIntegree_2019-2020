from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import Http404
from django.views.generic import FormView
from django.shortcuts import redirect
from django.utils.translation import gettext as _

from . import groups as groups_utils


# Access restriction mixins

class SelfStudentOnly(UserPassesTestMixin):
    # FIXME: Redirect self_student and back_office_members to 404
    """Restrict view access to the related student."""

    def test_func(self):
        """Check if the user's 'pk' matches with the url.GET.get('pk')
        value."""

        return self.request.user.student_rr.pk == self.kwargs["pk"]

    def handle_no_permission(self):
        """Raise a 404."""

        raise Http404


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


# Autofill 'created_by' formfield mixins (form and view)

class HideCreatedByFieldFormMixin(forms.ModelForm):
    """Mixin for ModelForms thats hide the 'created_by' field.

    The 'created_by'-field is still created and can be populated by the view
    without an input from the user.
    """

    class Meta:
        """Meta definition for HideCreatedByFieldFormMixin."""

        widgets = {
            'created_by': forms.HiddenInput(),
        }


class AutofillCreatedByRequestUser(FormView):
    """Autofill the 'created_by'-formfield by the request.user."""

    def get_initial(self):
        """Returns the initial data to use for forms on this view."""

        initial = super().get_initial()
        initial['created_by'] = self.request.user
        return initial


# FormFields mixins

class VerboseModuleChoiceField(forms.ModelChoiceField):
    """Display the reference and the title of each module in a verbose format
    in the ChoiceField."""

    def label_from_instance(self, module):
        """Return the verbose value."""

        return "{} ({})".format(module.title, module.reference)
