from django.contrib import admin
from django.utils.translation import ugettext as _

from .models import Module, ModuleLevel


class ModuleAdmin(admin.ModelAdmin):
    """UserProfile admin registration class."""

    model = Module


class ModuleLevelAdmin(admin.ModelAdmin):
    """UserProfile admin registration class."""

    model = ModuleLevel


admin.site.register(Module, ModuleAdmin)
admin.site.register(ModuleLevel, ModuleLevelAdmin)
