from django.contrib import admin
from django.utils.translation import ugettext as _

from .models import Degree, DegreeCategory, Module, ModuleLevel


admin.site.register(Degree)
admin.site.register(DegreeCategory)
admin.site.register(Module)
admin.site.register(ModuleLevel)
