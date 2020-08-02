from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView, ListView

from ..forms import ClassroomForm
from ..models import Classroom
from .resource import (
    BackOfficeResourceCreateViewMixin,
    BackOfficeResourceUpdateViewMixin,
)
from registration.utils.mixins import ManagerAdministratorOnlyMixin


class ClassroomListView(LoginRequiredMixin, ManagerAdministratorOnlyMixin,
                        ListView):  # TODO: Debug view
    """ListView for Classroom."""

    model = Classroom
    template_name = "management/room/classroom_listview.html"
    context_object_name = "classrooms"
    paginate_by = 10


class ClassroomDetailView(LoginRequiredMixin, ManagerAdministratorOnlyMixin,
                          DetailView):  # TODO: Debug view
    """DetailView for Classroom."""

    model = Classroom
    template_name = "management/room/classroom_detailview.html"
    context_object_name = "classroom"


class ClassroomCreateView(LoginRequiredMixin, ManagerAdministratorOnlyMixin,
                          BackOfficeResourceCreateViewMixin):  # TODO: Debug view
    """CreateView for Classroom."""

    model = Classroom
    form_class = ClassroomForm
    template_name = "management/room/classroom_createview.html"


class ClassroomUpdateView(LoginRequiredMixin, ManagerAdministratorOnlyMixin,
                          BackOfficeResourceUpdateViewMixin):  # TODO: Debug view
    """UpdateView for Classroom."""

    model = Classroom
    form_class = ClassroomForm
    context_object_name = "classroom"
    template_name = "management/room/classroom_updateview.html"


class ClassroomDeleteView(LoginRequiredMixin, ManagerAdministratorOnlyMixin,
                          DeleteView):  # TODO: Debug view
    """DeleteView for Classroom."""

    model = Classroom
    context_object_name = "classroom"
    template_name = "management/room/classroom_deleteview.html"
    success_url = reverse_lazy('classroom_listview')
