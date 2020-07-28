from django.shortcuts import render
from django.views.generic import DetailView, ListView

from ..models import Degree, DegreeCategory


class DegreeListView(ListView):  # TODO: Debug view
    """ListView for Modules"""

    model = Degree
    template_name = "management/degree_listview.html"
    context_object_name = "degrees"
    paginate_by = 10


class DegreeDetailView(DetailView):  # TODO: Debug view
    """DetailView for Modules"""

    model = Degree
    template_name = "management/degree_detailview.html"
    context_object_name = "degree"
