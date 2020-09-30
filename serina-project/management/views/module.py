from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView, ListView

from ..forms import ModuleCreateForm, ModuleUpdateForm, ModuleLevelForm
from ..models import Module, ModuleLevel
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
