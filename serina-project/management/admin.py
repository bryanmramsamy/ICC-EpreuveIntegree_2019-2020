from django.contrib import admin
from django.utils.translation import ugettext as _

from .models import Curriculum, CurriculumCategory, Module, ModuleLevel


# class CurriculumAdmin(admin.ModelAdmin):
#     """Curriculum admin registration class."""

#     model = Curriculum


# class CurriculumCategoryAdmin(admin.ModelAdmin):
#     """CurriculumCategory admin registration class."""

#     model = CurriculumCategory


# class ModuleAdmin(admin.ModelAdmin):
#     """ModuleAdmin admin registration class."""

#     model = Module


# class ModuleLevelAdmin(admin.ModelAdmin):
#     """ModuleLevelAdmin admin registration class."""

#     model = ModuleLevel


# admin.site.register(Curriculum, CurriculumAdmin)
# admin.site.register(CurriculumCategory, CurriculumCategoryAdmin)
# admin.site.register(Module, ModuleAdmin)
# admin.site.register(ModuleLevel, ModuleLevelAdmin)
