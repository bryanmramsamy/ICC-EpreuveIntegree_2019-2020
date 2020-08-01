from django.shortcuts import render
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
)

from ..forms import *
from ..models import Course


class CourseListView(ListView):  # TODO: Debug view
    """ListView for Course."""

    model = Course
    template_name = "management/course/course_listview.html"
    context_object_name = "courses"
    paginate_by = 10


class CourseDetailView(DetailView):  # TODO: Debug view
    """DetailView for Course."""

    model = Course
    template_name = "management/course/course_detailview.html"
    context_object_name = "course"
