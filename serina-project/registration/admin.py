from django.contrib import admin
from django.utils.translation import ugettext as _

from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    """UserProfile admin register class"""

    # Listview

    list_display = (
        'user',
        'user_last_name',
        'user_first_name',
        'birthday',
        'nationality',
        'postalData'
    )
    list_filter = ('nationality',)

    ordering = ('user', 'nationality')
    search_fields = ('user', 'postalCode', 'postalLocality')
    date_hierarchy = 'birthday'

    def user_last_name(self, userProfile):
        """Display user's last name in column"""

        return userProfile.user.last_name

    def user_first_name(self, userProfile):
        """Display user's first name in column"""

        return userProfile.user.first_name

    def postalData(self, userProfile):
        """Display user's last name in column"""

        return "{} {}".format(userProfile.postalCode,
                              userProfile.postalLocality)

    user_last_name.short_description = _('Last name')
    user_first_name.short_description = _('First name')
    postalData.short_description = _('Postal locality')

    # Detailview

    readonly_fields = ['user']

    fieldsets = (
        (_('General information'), {
            'description': _("User profile's general informations"),
            'fields': ('user', 'birthday', 'nationality', 'address',
                       'postalCode', 'postalLocality')
        }),
    )


admin.site.register(UserProfile, UserProfileAdmin)
