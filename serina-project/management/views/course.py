from django.shortcuts import render
from django.views.generic import DetailView, ListView

from ..models import Course


class CourseListView(ListView):  # TODO: Debug view
    """ListView for Classroom."""

    model = Course
    template_name = "management/course_listview.html"
    context_object_name = "courses"
    paginate_by = 10


class CourseDetailView(DetailView):  # TODO: Debug view
    """DetailView for Classroom."""

    model = Course
    template_name = "management/course_detailview.html"
    context_object_name = "course"
