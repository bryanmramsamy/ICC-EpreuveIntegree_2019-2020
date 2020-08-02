from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView, ListView

from ..forms import CourseCreateForm, CourseUpdateForm
from ..models import Course
from .resource import (
    BackOfficeResourceCreateViewMixin,
    BackOfficeResourceUpdateViewMixin,
)


class CourseListView(ListView):  # TODO: Debug view
    """ListView for Course."""

    model = Course
    context_object_name = "courses"
    template_name = "management/course/course_listview.html"
    paginate_by = 10


class CourseDetailView(DetailView):  # TODO: Debug view
    """DetailView for Course."""

    model = Course
    context_object_name = "course"
    template_name = "management/course/course_detailview.html"


class CourseCreateView(BackOfficeResourceCreateViewMixin):  # TODO: Debug view
    """CreateView for Course."""

    model = Course
    form_class = CourseCreateForm
    template_name = "management/course/course_createview.html"


class CourseUpdateView(BackOfficeResourceUpdateViewMixin):  # TODO: Debug view
    """UpdateView for Course."""

    model = Course
    form_class = CourseUpdateForm
    context_object_name = "course"
    template_name = "management/course/course_updateview.html"


class CourseDeleteView(DeleteView):  # TODO: Debug view
    """DeleteView for Course."""

    model = Course
    context_object_name = "course"
    template_name = "management/course/course_deleteview.html"
    success_url = reverse_lazy('course_listview')
