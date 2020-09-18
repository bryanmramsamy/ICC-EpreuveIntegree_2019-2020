from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView, ListView

from ..forms import CourseCreateForm, CourseUpdateForm
from ..models import Course
from .resource import (
    BackOfficeResourceCreateViewMixin,
    BackOfficeResourceUpdateViewMixin,
)
from registration.models import ModuleRegistrationReport
from registration.utils.mixins import ManagerAdministratorOnlyMixin


class CourseListView(ListView):
    """ListView for Course."""

    model = Course
    context_object_name = "courses"
    template_name = "management/course/course_listview.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        """Add number of active courses to the context."""

        context = super().get_context_data(**kwargs)
        context["nb_active_courses"] = len(
            [course.status for course in Course.objects.all()],
        )
        return context


class CourseDetailView(DetailView):
    """DetailView for Course."""

    model = Course
    context_object_name = "course"
    template_name = "management/course/course_detailview.html"

    def get_context_data(self, **kwargs):
        """Add the related module registration request to the context."""

        context = super().get_context_data(**kwargs)
        context["modules_rrs"] = ModuleRegistrationReport.objects.filter(
            Q(course=self.object),
            (Q(status="APPROVED") | Q(status="PAYED") | Q(status="COMPLETED")),
        )

        return context


class CourseCreateView(LoginRequiredMixin, ManagerAdministratorOnlyMixin,
                       BackOfficeResourceCreateViewMixin):
    """CreateView for Course."""

    model = Course
    form_class = CourseCreateForm
    template_name = "management/course/course_createview.html"


class CourseUpdateView(LoginRequiredMixin, ManagerAdministratorOnlyMixin,
                       BackOfficeResourceUpdateViewMixin):
    """UpdateView for Course."""

    model = Course
    form_class = CourseUpdateForm
    context_object_name = "course"
    template_name = "management/course/course_updateview.html"


class CourseDeleteView(LoginRequiredMixin, ManagerAdministratorOnlyMixin,
                       DeleteView):
    """DeleteView for Course."""

    model = Course
    context_object_name = "course"
    template_name = "management/course/course_deleteview.html"
    success_url = reverse_lazy('course_listview')
