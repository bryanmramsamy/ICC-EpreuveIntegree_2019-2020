from django.shortcuts import render
from django.views.generic import ListView

from .models import Module, ModuleLevel


def home(request):
    """Homepage render."""

    # TODO: Debug view
    return render(request, "management/home.html", {})


class ModuleListView(ListView):
    """ListView for Modules"""

    # TODO: Debug view
    model = Module
    template_name = "management/module_listview.html"
    context_object_name = "modules"
    paginate_by = 10
