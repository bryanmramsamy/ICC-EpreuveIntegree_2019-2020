from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    DeleteView,
    DetailView,
    ListView,
)

from ..forms import ModuleCreateForm, ModuleUpdateForm, ModuleLevelForm
from ..models import Module, ModuleLevel
from .resource import BackOfficeResourceCreateViewMixin, BackOfficeResourceUpdateViewMixin


# Module views

class ModuleListView(ListView):  # TODO: Debug view
    """ListView for Modules."""

    model = Module
    template_name = "management/module/module_listview.html"
    context_object_name = "modules"
    paginate_by = 10


class ModuleDetailView(DetailView):  # TODO: Debug view
    """DetailView for Modules."""

    model = Module
    template_name = "management/module/module_detailview.html"
    context_object_name = "module"


class ModuleCreateView(BackOfficeResourceCreateViewMixin):
    """CreateView for Modules."""

    model = Module
    form_class = ModuleCreateForm
    template_name = "management/module/module_createview.html"


class ModuleUpdateView(BackOfficeResourceUpdateViewMixin):
    """CreateView for Modules."""

    model = Module
    form_class = ModuleUpdateForm
    template_name = "management/module/module_createview.html"


class ModuleDeleteView(DeleteView):
    """"""

    model = Module
    template_name = "management/module/module_deleteview.html"
    context_object_name = "module"
    success_url = reverse_lazy('module_listview')

# ModuleLevel Views

class ModuleLevelListView(ListView):  # TODO: Debug view
    """ListView for ModuleLevels."""

    model = ModuleLevel
    template_name = "management/module/modulelevel_listview.html"
    context_object_name = "levels"


class ModuleLevelDetailView(DetailView):  # TODO: Debug view
    """DetailView for ModuleLevels."""

    model = ModuleLevel
    template_name = "management/module/modulelevel_detailview.html"
    context_object_name = "level"


class ModuleLevelCreateView(BackOfficeResourceCreateViewMixin):
    """CreateView for ModuleLevels."""

    model = ModuleLevel
    form_class = ModuleLevelForm
    template_name = "management/module/modulelevel_createview.html"
