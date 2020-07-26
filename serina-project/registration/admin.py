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
        'is_back_office_user'
    )

    list_filter = ('groups', 'is_active', 'userprofile__nationality')

    ordering = ('-date_joined', 'username')
    search_fields = ('username', 'first_name', 'last_name')
    date_hierarchy = 'date_joined'

    def main_group(self, user):
        """Display the user's main group."""

        return groups_utils.main_group_i18n(user)

    main_group.short_description = _('Groups')

    def is_back_office_user(self, user):
        """Display if the user is a back-office user."""

        return groups_utils.is_back_office_user(user)

    is_back_office_user.boolean = True
    is_back_office_user.short_description = _('Back-Office user')


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
