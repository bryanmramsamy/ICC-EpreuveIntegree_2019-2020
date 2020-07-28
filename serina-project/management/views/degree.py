from django.shortcuts import render
from django.views.generic import DetailView, ListView

from ..models import Degree, DegreeCategory


class DegreeListView(ListView):  # TODO: Debug view
    """ListView for Degree."""

    model = Degree
    template_name = "management/degree_listview.html"
    context_object_name = "degrees"
    paginate_by = 10


class DegreeDetailView(DetailView):  # TODO: Debug view
    """DetailView for Degree."""

    model = Degree
    template_name = "management/degree_detailview.html"
    context_object_name = "degree"


class DegreeCategoryListView(ListView):  # TODO: Debug view
    """ListView for DegreeCategory."""

    model = DegreeCategory
    template_name = "management/degreecategory_listview.html"
    context_object_name = "categories"
    paginate_by = 10


class DegreeCategoryDetailView(DetailView):  # TODO: Debug view
    """DetailView for DegreeCategory."""

    model = DegreeCategory
    template_name = "management/degreecategory_detailview.html"
    context_object_name = "category"
