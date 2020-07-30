from django.contrib import admin

from .models import (
    DegreeRegistrationReport,
    ModuleRegistrationReport,
    StudentRegistrationReport,
)


admin.site.register(DegreeRegistrationReport)
admin.site.register(ModuleRegistrationReport)
admin.site.register(StudentRegistrationReport)
