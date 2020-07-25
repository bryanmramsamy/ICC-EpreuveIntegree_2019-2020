from django.contrib import admin
from django.utils.translation import ugettext as _

from .models import Module, ModuleLevel


admin.site.register(Module)
admin.site.register(ModuleLevel)
