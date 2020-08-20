from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView, ListView

from ..forms import ModuleCreateForm, ModuleUpdateForm, ModuleLevelForm
from ..models import Module, ModuleLevel
from .resource import (
    BackOfficeResourceCreateViewMixin,
    BackOfficeResourceUpdateViewMixin,
)
from registration.utils.mixins import ManagerAdministratorOnlyMixin


# Module views

class ModuleListView(ListView):
    """ListView for Modules."""

    model = Module
    context_object_name = "modules"
    template_name = "management/module/module_listview.html"
    paginate_by = 10


class ModuleDetailView(DetailView):
    """DetailView for Modules."""

    model = Module
    context_object_name = "module"
    template_name = "management/module/module_detailview.html"


class ModuleCreateView(LoginRequiredMixin, ManagerAdministratorOnlyMixin,
                       BackOfficeResourceCreateViewMixin):
    """CreateView for Modules."""

    model = Module
    form_class = ModuleCreateForm
    template_name = "management/module/module_createview.html"


class ModuleUpdateView(LoginRequiredMixin, ManagerAdministratorOnlyMixin,
                       BackOfficeResourceUpdateViewMixin):
    """UpdateView for Modules."""

    model = Module
    form_class = ModuleUpdateForm
    context_object_name = "module"
    template_name = "management/module/module_updateview.html"


class ModuleDeleteView(LoginRequiredMixin, ManagerAdministratorOnlyMixin,
                       DeleteView):
    """DeleteView for Modules."""

    model = Module
    context_object_name = "module"
    template_name = "management/module/module_deleteview.html"
    success_url = reverse_lazy('module_listview')


# ModuleLevel Views

class ModuleLevelListView(ListView):
    """ListView for ModuleLevels."""

    model = ModuleLevel
    context_object_name = "levels"
    template_name = "management/module/modulelevel_listview.html"


class ModuleLevelDetailView(DetailView):
    """DetailView for ModuleLevels."""

    model = ModuleLevel
    context_object_name = "level"
    template_name = "management/module/modulelevel_detailview.html"


class ModuleLevelCreateView(LoginRequiredMixin, ManagerAdministratorOnlyMixin,
                            BackOfficeResourceCreateViewMixin):
    """CreateView for ModuleLevels."""

    model = ModuleLevel
    form_class = ModuleLevelForm
    template_name = "management/module/modulelevel_createview.html"


class ModuleLevelUpdateView(LoginRequiredMixin, ManagerAdministratorOnlyMixin,
                            BackOfficeResourceUpdateViewMixin):
    """UpdateView for ModuleLevels."""

    model = ModuleLevel
    form_class = ModuleLevelForm
    context_object_name = "level"
    template_name = "management/module/modulelevel_updateview.html"


class ModuleLevelDeleteView(LoginRequiredMixin, ManagerAdministratorOnlyMixin,
                            DeleteView):
    """DeleteView for ModuleLevels."""

    model = ModuleLevel
    template_name = "management/module/modulelevel_deleteview.html"
    context_object_name = "level"
    success_url = reverse_lazy('modulelevel_listview')
