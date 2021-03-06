from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView, ListView

from ..forms import CourseCreateForm, CourseUpdateForm
from ..models import Classroom, Course, Module
from .resource import (
    BackOfficeResourceCreateViewMixin,
    BackOfficeResourceUpdateViewMixin,
)
from registration.models import ModuleRegistrationReport
from registration.utils.mixins import (
    ManagerAdministratorOnlyMixin,
    StudentOnlyMixin,
    TeacherOnlyMixin,
)


class CourseListView(ListView):
    """ListView for Course."""

    model = Course
    context_object_name = "courses"
    template_name = "management/course/course_listview.html"
    paginate_by = settings.PAGINATION["listview"]

    def get_queryset(self):
        """Apply filters if submitted by user."""

        # GET variables
        search_module = self.request.GET.get('q_module')
        search_teacher = self.request.GET.get('q_teacher')
        search_room = self.request.GET.get('q_room')

        # Main query
        query_result = Course.objects.all()

        # Filtering
        if search_module:
            query_result = query_result.filter(module=search_module)
        if search_teacher:
            query_result = query_result.filter(teacher=search_teacher)
        if search_room:
            query_result = query_result.filter(room=search_room)

        # Query result
        return query_result

    def get_context_data(self, **kwargs):
        """Add search values to context."""

        context = super().get_context_data(**kwargs)

        # GET variables for search filters
        context['q_module'] = self.request.GET.get('q_module')
        context['q_teacher'] = self.request.GET.get('q_teacher')
        context['q_room'] = self.request.GET.get('q_room')

        # Search values
        context['s_modules'] = Module.objects.all()
        context['s_teachers'] = User.objects.filter(groups__name="Teacher")
        context['s_rooms'] = Classroom.objects.all()

        context["nb_active_courses"] = len(
            [course.status for course in Course.objects.all()],
        )
        return context


class StudentCourseListView(
    LoginRequiredMixin,
    StudentOnlyMixin,
    CourseListView
):
    """Course detailed view for student.

    Ony the student's courses will be displayed.
    """

    def get_queryset(self):
        """Get the courses of the student only."""

        return Course.objects.filter(modules_rrs__student_rr__created_by=self.request.user)


class TeacherCourseListView(
    LoginRequiredMixin,
    TeacherOnlyMixin,
    CourseListView
):
    """Course detailed view for student.

    Ony the student's courses will be displayed.
    """

    def get_queryset(self):
        """Get the courses of the student only."""

        return Course.objects.filter(teacher=self.request.user)


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

    def get_context_data(self, **kwargs):
        """Add modules, teachers and classrooms to context for select field."""

        context = super().get_context_data(**kwargs)
        context["modules"] = Module.objects.all()
        context["teachers"] = User.objects.filter(groups__name="Teacher")
        context["rooms"] = Classroom.objects.all()
        return context


class CourseUpdateView(LoginRequiredMixin, ManagerAdministratorOnlyMixin,
                       BackOfficeResourceUpdateViewMixin):
    """UpdateView for Course."""

    model = Course
    form_class = CourseUpdateForm
    context_object_name = "course"
    template_name = "management/course/course_updateview.html"

    def get_context_data(self, **kwargs):
        """Add modules, teachers and classrooms to context for select field.

        Teachers are filtered by the chosen modules.
        """

        context = super().get_context_data(**kwargs)
        context["modules"] = Module.objects.all()
        context["teachers"] = User.objects.filter(groups__name="Teacher") \
            .filter(teachable_modules=self.object.module)
        context["rooms"] = Classroom.objects.all()
        return context


class CourseDeleteView(LoginRequiredMixin, ManagerAdministratorOnlyMixin,
                       DeleteView):
    """DeleteView for Course."""

    model = Course
    context_object_name = "course"
    template_name = "management/course/course_deleteview.html"
    success_url = reverse_lazy('course_listview')
