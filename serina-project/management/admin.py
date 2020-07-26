from django.contrib import admin
from django.utils.translation import ugettext as _

from .models import (
    Classroom,
    Course,
    Degree,
    DegreeCategory,
    Module,
    ModuleLevel
)


admin.site.register(Classroom)
admin.site.register(Course)
admin.site.register(Degree)
admin.site.register(DegreeCategory)
admin.site.register(Module)
admin.site.register(ModuleLevel)
