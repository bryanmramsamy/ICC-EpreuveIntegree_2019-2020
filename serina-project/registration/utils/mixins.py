from django import forms
from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.views.generic import FormView
from django.shortcuts import redirect
from django.utils.translation import gettext as _

from .. import models
from . import groups as groups_utils
from . import messages as messages_utils
from rating import models as rating_models


# Access restriction mixins


class AccessRestrictionMixin(UserPassesTestMixin):
    """Redirect to the 403 page."""

    def handle_no_permission(self):
        """Raise the 403 error."""

        raise PermissionDenied


class StudentOnlyMixin(AccessRestrictionMixin):
    """Restrict view access to Students users."""

    def test_func(self):
        """Check if the user is a registered student user."""

        return groups_utils.is_student(self.request.user)


class BackOfficeUsersOnlyMixin(AccessRestrictionMixin):
    """Restrict view access to Back-Office users."""

    def test_func(self):
        """Check if the user is a Back-Office user."""

        return groups_utils.is_back_office_user(self.request.user)


class ManagerAdministratorOnlyMixin(AccessRestrictionMixin):
    """Restrict view access to 'Manager'-group members and
    'Administrator'-group members."""

    def test_func(self):
        """Check if the user is a Manager or an Administrator."""

        return groups_utils.is_manager_or_administrator(self.request.user)


class StudentManagerAdministratorOnlyMixin(ManagerAdministratorOnlyMixin):
    """Restrict view access to 'Student'-group members, the 'Manager'-group
    members and 'Administrator'-group members."""

    def test_func(self):
        """Check if the user is a Student, Manager or an Administrator."""

        return super(StudentManagerAdministratorOnlyMixin, self).test_func() \
            or groups_utils.is_student(self.request.user)


class SelfStudentManagerAdministratorOnlyMixin(
    StudentManagerAdministratorOnlyMixin,
):
    """Restrict view access to 'Manager'-group members and
    'Administrator'-group members and the student who created the object.

    This mixins works for students, modules and degrees regitrations reports.
    """

    def test_func(self):
        """Check if the user is a Student, Manager or an Administrator. If the
        user is a student, check if (s)he is the one who created the object.

        The object being variable, the queryset is adapted according to the
        object-type received.
        """

        super_test_valid = super(SelfStudentManagerAdministratorOnlyMixin,
                                 self).test_func()
        self_test_valid = False

        # Check if user is a student

        if groups_utils.is_student(self.request.user):

            # StudentRegistrationReport

            if type(self.get_object()) is models.student_rr \
                                                .StudentRegistrationReport:
                self_test_valid = \
                    self.request.user.student_rr.pk == self.get_object().pk

            # ModuleRegistrationReport

            elif type(self.get_object()) is models.module_rr \
                                                  .ModuleRegistrationReport:
                self_test_valid = self.request.user.student_rr.modules_rrs \
                                      .filter(pk=self.get_object().pk) \
                                      .exists()

            # DegreeRegistrationReport

            elif type(self.get_object()) is models.degree_rr \
                                                  .DegreeRegistrationReport:
                self_test_valid = self.request.user.student_rr.degrees_rrs \
                                      .filter(pk=self.get_object().pk) \
                                      .exists()

            # StudentRating

            elif type(self.get_object()) is rating_models.StudentRating:
                self_test_valid = self.request.user.ratings.filter(
                    pk=self.get_object().pk).exists()

        # Otherwise user is manager or administrator

        else:
            self_test_valid = True

        return super_test_valid and self_test_valid


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

class VerboseDegreeModuleChoiceField(forms.ModelChoiceField):
    """Display the reference and the title of each degree or module in a
    verbose format as a ChoiceField."""

    def label_from_instance(self, degree_or_module):
        """Return the verbose value."""

        return "{} ({})".format(degree_or_module.title,
                                degree_or_module.reference)
