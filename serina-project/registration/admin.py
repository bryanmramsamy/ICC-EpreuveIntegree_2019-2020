from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group, User
from django.utils.translation import ugettext as _

from .models import UserProfile
from .utilities import groups_utils


class UserProfileAdmin(admin.StackedInline):
    """UserProfile admin registration class.

    This class is displayed as StackedInline with the
    django.contrib.auth.admin.UserAdmin class to force the administrator to
    fill the profile when a user instance is created or updated.
    """

    # StackedInline
    model = UserProfile
    can_delete = False
    verbose_name = _("User profile")
    verbose_name_plural = _("Users profile")

    # DetailView
    fields = ['user', 'birthday', 'nationality', 'address', 'postalCode',
              'postalLocality']


class CustomUserAdmin(UserAdmin):
    """Customized UserAdmin class.

    Integrates the UserProfileAdmin class in StackedInline.
    Display more fields in the admin ListView with custom search tools.
    """
    inlines = (UserProfileAdmin,)

    # Listview
    list_display = (
        'username',
        'first_name',
        'last_name',
        'email',
        'date_joined',
        'main_group',
        'is_member_of_promoted_group'
    )

    list_filter = ('groups', 'is_active', 'userprofile__nationality')

    ordering = ('-date_joined', 'username')
    search_fields = ('username', 'first_name', 'last_name')
    date_hierarchy = 'date_joined'

    def main_group(self, user):
        """Display main group of the user."""

        if user.groups.filter(name="Administrator").exists():
            main_group = _("Administrator")
        elif user.groups.filter(name="Manager").exists():
            main_group = _("Manager")
        elif user.groups.filter(name="Professor").exists():
            main_group = _("Professor")
        elif user.groups.filter(name="Student").exists():
            main_group = _("Student")
        else:
            main_group = _("Guest")

        return main_group

    main_group.short_description = _('Groups')

    def is_member_of_promoted_group(self, user):
        """Display if the user is member of a promoted group.

        The promoted groups are: 'Professor', 'Manager', 'Administrator'."""

        return groups_utils.is_member_of_promoted_group(user)

    is_member_of_promoted_group.boolean = True
    is_member_of_promoted_group.short_description = _('Promoted user')


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
