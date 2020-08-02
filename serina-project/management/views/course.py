from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView, ListView

from ..forms import CourseCreateForm, CourseUpdateForm
from ..models import Course
from .resource import (
    BackOfficeResourceCreateViewMixin,
    BackOfficeResourceUpdateViewMixin,
)
from registration.utils.mixins import ManagerAdministratorOnlyMixin


class CourseListView(LoginRequiredMixin, ManagerAdministratorOnlyMixin,
                     ListView):  # TODO: Debug view
    """ListView for Course."""

    model = Course
    context_object_name = "courses"
    template_name = "management/course/course_listview.html"
    paginate_by = 10


class CourseDetailView(LoginRequiredMixin, ManagerAdministratorOnlyMixin,
                       DetailView):  # TODO: Debug view
    """DetailView for Course."""

    model = Course
    context_object_name = "course"
    template_name = "management/course/course_detailview.html"


class CourseCreateView(LoginRequiredMixin, ManagerAdministratorOnlyMixin,
                       BackOfficeResourceCreateViewMixin):  # TODO: Debug view
    """CreateView for Course."""

    model = Course
    form_class = CourseCreateForm
    template_name = "management/course/course_createview.html"


class CourseUpdateView(LoginRequiredMixin, ManagerAdministratorOnlyMixin,
                       BackOfficeResourceUpdateViewMixin):  # TODO: Debug view
    """UpdateView for Course."""

    model = Course
    form_class = CourseUpdateForm
    context_object_name = "course"
    template_name = "management/course/course_updateview.html"


class CourseDeleteView(LoginRequiredMixin, ManagerAdministratorOnlyMixin,
                       DeleteView):  # TODO: Debug view
    """DeleteView for Course."""

    model = Course
    context_object_name = "course"
    template_name = "management/course/course_deleteview.html"
    success_url = reverse_lazy('course_listview')
