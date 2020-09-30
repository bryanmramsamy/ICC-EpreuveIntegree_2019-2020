from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView, ListView

from ..forms import ModuleCreateForm, ModuleUpdateForm, ModuleLevelForm
from ..models import Degree, Module, ModuleLevel
from .resource import (
    BackOfficeResourceCreateViewMixin,
    BackOfficeResourceUpdateViewMixin,
)
from rating.models import StudentRating
from registration.utils import groups, registration
from registration.utils.mixins import ManagerAdministratorOnlyMixin


# Module views

class ModuleListView(ListView):
    """ListView for Modules."""

    model = Module
    context_object_name = "modules"
    template_name = "management/module/module_listview.html"
    paginate_by = settings.PAGINATION["listview"]

    def get_queryset(self):
        """Apply filters if submitted by user."""

        # GET variables
        search_title_reference_description = self.request.GET.get(
            'q_title_reference_description',
        )
        search_level = self.request.GET.get('q_level')
        search_prerequisite = self.request.GET.get('q_prerequisite')
        search_degree = self.request.GET.get('q_degree')
        search_teacher = self.request.GET.get('q_teacher')

        # Main query
        query_result = Module.objects.all()

        # Filtering
        if search_title_reference_description:
            query_result = query_result.filter(
                Q(title__icontains=search_title_reference_description)
                | Q(reference__icontains=search_title_reference_description)
                | Q(description__icontains=search_title_reference_description)
            )
        if search_level:
            query_result = query_result.filter(level=search_level)
        if search_prerequisite:
            query_result = query_result.filter(
                prerequisites=search_prerequisite,
            )
        if search_degree:
            query_result = query_result.filter(
                degrees=search_degree,
            )
        if search_teacher:
            query_result = query_result.filter(
                eligible_teachers=search_teacher,
            )

        # Query result
        return query_result

    def get_context_data(self, **kwargs):
        """Add search values to context."""

        context = super().get_context_data(**kwargs)

        # GET variables for search filters
        context['q_title_reference_description'] = self.request.GET.get(
            'q_title_reference_description',
        )
        context['q_level'] = self.request.GET.get('q_level')
        context['q_prerequisite'] = self.request.GET.get('q_prerequisite')
        context['q_degree'] = self.request.GET.get('q_degree')
        context['q_teacher'] = self.request.GET.get('q_teacher')

        # Search values
        context['s_levels'] = ModuleLevel.objects.all()
        context['s_prerequisites'] = Module.objects.all()
        context['s_degrees'] = Degree.objects.all()
        context['s_teachers'] = User.objects.filter(groups__name="Teacher")

        return context


class ModuleDetailView(DetailView):
    """DetailView for Modules."""

    model = Module
    context_object_name = "module"
    template_name = "management/module/module_detailview.html"

    def get_context_data(self, **kwargs):
        """Add 'already_validated' and 'all_prerequisites_validated' to the
        context of each module."""

        context = super().get_context_data(**kwargs)

        context["already_validated"] = registration \
            .succeeded_module_rr_already_exists(self.request.user, self.object)

        context["all_prerequisites_validated"] = registration \
            .all_prerequisites_validated_by_user(self.request.user,
                                                 self.object)

        context["ratings"] = StudentRating.objects.filter(module=self.object)

        if not groups.is_manager_or_administrator(self.request.user):
            context["ratings"] = context["ratings"].filter(is_visible=True)
            context["student_rating"] = context["ratings"].filter(
                created_by=self.request.user
            ).last()

        return context


class ModuleCreateView(LoginRequiredMixin, ManagerAdministratorOnlyMixin,
                       BackOfficeResourceCreateViewMixin):
    """CreateView for Modules."""

    model = Module
    form_class = ModuleCreateForm
    template_name = "management/module/module_createview.html"

    def get_context_data(self, **kwargs):
        """Add all ModuleLevel to context for select input."""

        context = super().get_context_data(**kwargs)
        context["levels"] = ModuleLevel.objects.all()
        return context

    def get_success_url(self):
        """Redirect to the update view of the created module in order to add
        the prerequisites and the eligible teachers."""

        return reverse_lazy('module_updateview', kwargs={'pk': self.object.id})


class ModuleUpdateView(LoginRequiredMixin, ManagerAdministratorOnlyMixin,
                       BackOfficeResourceUpdateViewMixin):
    """UpdateView for Modules."""

    model = Module
    form_class = ModuleUpdateForm
    context_object_name = "module"
    template_name = "management/module/module_updateview.html"

    def get_context_data(self, **kwargs):
        """Add all ModuleLevel to context for select input."""

        context = super().get_context_data(**kwargs)
        context["levels"] = ModuleLevel.objects.all()
        context["teachers"] = User.objects.filter(groups__name="Teacher")
        context["prerequisites"] = Module.objects.exclude(pk=self.object.pk) \
            .exclude(prerequisites=self.object)

        return context


class ModuleDeleteView(LoginRequiredMixin, ManagerAdministratorOnlyMixin,
                       DeleteView):
    """DeleteView for Modules."""

    model = Module
    context_object_name = "module"
    template_name = "management/module/module_deleteview.html"
    success_url = reverse_lazy('module_listview')


# ModuleLevel Views

class ModuleLevelListView(ListView):
    """ListView for ModuleLevels."""

    model = ModuleLevel
    context_object_name = "levels"
    template_name = "management/module/modulelevel_listview.html"
    paginate_by = settings.PAGINATION["listview"]


class ModuleLevelDetailView(DetailView):
    """DetailView for ModuleLevels."""

    model = ModuleLevel
    context_object_name = "level"
    template_name = "management/module/modulelevel_detailview.html"


class ModuleLevelCreateView(LoginRequiredMixin, ManagerAdministratorOnlyMixin,
                            BackOfficeResourceCreateViewMixin):
    """CreateView for ModuleLevels."""

    model = ModuleLevel
    form_class = ModuleLevelForm
    template_name = "management/module/modulelevel_createview.html"


class ModuleLevelUpdateView(LoginRequiredMixin, ManagerAdministratorOnlyMixin,
                            BackOfficeResourceUpdateViewMixin):
    """UpdateView for ModuleLevels."""

    model = ModuleLevel
    form_class = ModuleLevelForm
    context_object_name = "level"
    template_name = "management/module/modulelevel_updateview.html"


class ModuleLevelDeleteView(LoginRequiredMixin, ManagerAdministratorOnlyMixin,
                            DeleteView):
    """DeleteView for ModuleLevels."""

    model = ModuleLevel
    template_name = "management/module/modulelevel_deleteview.html"
    context_object_name = "level"
    success_url = reverse_lazy('modulelevel_listview')
