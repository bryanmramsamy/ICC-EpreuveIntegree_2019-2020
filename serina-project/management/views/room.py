from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
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


class ClassroomListView(ListView):
    """ListView for Classroom."""

    model = Classroom
    template_name = "management/room/classroom_listview.html"
    context_object_name = "classrooms"
    paginate_by = settings.PAGINATION["listview"]

    def get_queryset(self):
        """Apply filters if submitted by user."""

        # GET variables
        search_name_reference_description = self.request.GET.get(
            'q_name_reference_description',
        )

        # Main query
        query_result = Classroom.objects.all()

        # Filtering
        if search_name_reference_description:
            query_result = query_result.filter(
                Q(name__icontains=search_name_reference_description)
                | Q(reference__icontains=search_name_reference_description)
                | Q(description__icontains=search_name_reference_description)
            )

        # Query result
        return query_result

    def get_context_data(self, **kwargs):
        """Add search values to context."""

        context = super().get_context_data(**kwargs)

        # GET variables for search filters
        context['q_name_reference_description'] = self.request.GET.get(
            'q_name_reference_description',
        )

        return context


class ClassroomDetailView(DetailView):
    """DetailView for Classroom."""

    model = Classroom
    template_name = "management/room/classroom_detailview.html"
    context_object_name = "classroom"


class ClassroomCreateView(LoginRequiredMixin, ManagerAdministratorOnlyMixin,
                          BackOfficeResourceCreateViewMixin):
    """CreateView for Classroom."""

    model = Classroom
    form_class = ClassroomForm
    template_name = "management/room/classroom_createview.html"


class ClassroomUpdateView(LoginRequiredMixin, ManagerAdministratorOnlyMixin,
                          BackOfficeResourceUpdateViewMixin):
    """UpdateView for Classroom."""

    model = Classroom
    form_class = ClassroomForm
    context_object_name = "classroom"
    template_name = "management/room/classroom_updateview.html"


class ClassroomDeleteView(LoginRequiredMixin, ManagerAdministratorOnlyMixin,
                          DeleteView):
    """DeleteView for Classroom."""

    model = Classroom
    context_object_name = "classroom"
    template_name = "management/room/classroom_deleteview.html"
    success_url = reverse_lazy('classroom_listview')
