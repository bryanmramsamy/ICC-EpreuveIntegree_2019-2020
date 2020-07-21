from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group, User
from django.utils.translation import ugettext as _

from .models import UserProfile


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
        'is_student',
        'is_professor',
        'is_manager',
        'is_admin',
        # 'main_group'  # TODO: Fix display main group: Only displays "Guest"
    )

    list_filter = ('groups', 'is_active', 'userprofile__nationality')

    ordering = ('-date_joined', 'username')
    search_fields = ('username', 'first_name', 'last_name')
    date_hierarchy = 'date_joined'

    def is_member(self, user, group):
        """Check if the current user is member of the given group."""

        return user.groups.filter(name=group).exists()

    def is_student(self, user):
        """Check if the user is a student."""

        return self.is_member(user, "Student")

    def is_professor(self, user):
        """Check if the user is a professor."""

        return self.is_member(user, "Professor")

    def is_manager(self, user):
        """Check if the user is a manager."""

        return self.is_member(user, "Manager")

    def is_admin(self, user):
        """Check if the user is an administrator."""

        return user.is_staff

    # def main_group(self, user):
    #     if self.is_manager(user):
    #         main_group = _("Administrator")
    #     if self.is_professor:
    #         main_group = _("Professor")
    #     if self.is_student(user):
    #         main_group = _("Student")
    #     else:
    #         main_group = _("Guest")

    #     return main_group

    is_student.boolean = True
    is_student.short_description = _('Student')

    is_professor.boolean = True
    is_professor.short_description = _('Professor')

    is_manager.boolean = True
    is_manager.short_description = _('Manager')

    is_admin.boolean = True
    is_admin.short_description = _('Administrator')


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
