from django.shortcuts import render
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
)

from ..forms import ModuleForm, ModuleLevelForm
from ..models import Module, ModuleLevel


# Module views

class ModuleListView(ListView):  # TODO: Debug view
    """ListView for Modules."""

    model = Module
    template_name = "management/module_listview.html"
    context_object_name = "modules"
    paginate_by = 10


class ModuleDetailView(DetailView):  # TODO: Debug view
    """DetailView for Modules."""

    model = Module
    template_name = "management/module_detailview.html"
    context_object_name = "module"


class ModuleCreateView(CreateView):
    """CreateView for Modules."""

    model = Module
    form_class = ModuleForm
    template_name = "management/module_createview.html"


# ModuleLevel Views

class ModuleLevelListView(ListView):  # TODO: Debug view
    """ListView for ModuleLevels."""

    model = ModuleLevel
    template_name = "management/modulelevel_listview.html"
    context_object_name = "levels"


class ModuleLevelDetailView(DetailView):  # TODO: Debug view
    """DetailView for ModuleLevels."""

    model = ModuleLevel
    template_name = "management/modulelevel_detailview.html"
    context_object_name = "level"


class ModuleLevelCreateView(CreateView):
    # FIXME: Doesn't add object to database
    """CreateView for ModuleLevels."""

    model = ModuleLevel
    fields = '__all__'
    template_name = "management/modulelevel_createview.html"

    # def form_valid(self, form):
    #     model = form.save(commit=False)
    #     model.created_by = self.request.user
    #     model.save()
    #     return super(ModuleLevelCreateView, self).form_valid(form)
