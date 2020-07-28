from django.shortcuts import render
from django.views.generic import DetailView, ListView

from ..models import Classroom


class ClassroomListView(ListView):  # TODO: Debug view
    """ListView for Classroom."""

    model = Classroom
    template_name = "management/classroom_listview.html"
    context_object_name = "classrooms"
    paginate_by = 10


class ClassroomDetailView(DetailView):  # TODO: Debug view
    """DetailView for Classroom."""

    model = Classroom
    template_name = "management/classroom_detailview.html"
    context_object_name = "classroom"
