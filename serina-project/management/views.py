from django.shortcuts import render
from django.views.generic import ListView

from .models import Degree, DegreeCategory, Module, ModuleLevel


def home(request):  # TODO: Debug view
    """Homepage render."""

    return render(request, "management/home.html", {})


class DegreeListView(ListView):  # TODO: Debug view
    """ListView for Modules"""

    model = Degree
    template_name = "management/degree_listview.html"
    context_object_name = "degrees"
    paginate_by = 10


class ModuleListView(ListView):  # TODO: Debug view
    """ListView for Modules"""

    model = Module
    template_name = "management/module_listview.html"
    context_object_name = "modules"
    paginate_by = 10
