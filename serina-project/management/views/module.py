from django.shortcuts import render
from django.views.generic import DetailView, ListView

from ..models import Module, ModuleLevel


class ModuleListView(ListView):  # TODO: Debug view
    """ListView for Modules"""

    model = Module
    template_name = "management/module_listview.html"
    context_object_name = "modules"
    paginate_by = 10


class ModuleDetailView(DetailView):  # TODO: Debug view
    """DetailView for Modules"""

    model = Module
    template_name = "management/module_detailview.html"
    context_object_name = "module"
