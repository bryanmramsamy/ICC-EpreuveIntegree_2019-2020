from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView, ListView

from ..forms import ClassroomForm
from ..models import Classroom
from .resource import (
    BackOfficeResourceCreateViewMixin,
    BackOfficeResourceUpdateViewMixin,
)


class ClassroomListView(ListView):  # TODO: Debug view
    """ListView for Classroom."""

    model = Classroom
    template_name = "management/room/classroom_listview.html"
    context_object_name = "classrooms"
    paginate_by = 10


class ClassroomDetailView(DetailView):  # TODO: Debug view
    """DetailView for Classroom."""

    model = Classroom
    template_name = "management/room/classroom_detailview.html"
    context_object_name = "classroom"


class ClassroomCreateView(BackOfficeResourceCreateViewMixin):  # TODO: Debug view
    """CreateView for Classroom."""

    model = Classroom
    form_class = ClassroomForm
    template_name = "management/room/classroom_createview.html"


class ClassroomUpdateView(BackOfficeResourceUpdateViewMixin):  # TODO: Debug view
    """UpdateView for Classroom."""

    model = Classroom
    form_class = ClassroomForm
    context_object_name = "classroom"
    template_name = "management/room/classroom_updateview.html"


class ClassroomDeleteView(DeleteView):  # TODO: Debug view
    """DeleteView for Classroom."""

    model = Classroom
    context_object_name = "classroom"
    template_name = "management/room/classroom_deleteview.html"
    success_url = reverse_lazy('classroom_listview')
