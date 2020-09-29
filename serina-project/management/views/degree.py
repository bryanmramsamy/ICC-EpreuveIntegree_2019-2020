from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import DeleteView, DetailView, ListView

from ..forms import DegreeCreateForm, DegreeCategoryForm, DegreeUpdateForm
from ..models import Degree, DegreeCategory, Module
from .resource import (
    BackOfficeResourceCreateViewMixin,
    BackOfficeResourceUpdateViewMixin,
)
from rating.models import StudentRating
from registration.utils import groups as group_utils
from registration.utils.mixins import ManagerAdministratorOnlyMixin


# Degree

class DegreeListView(ListView):
    """ListView for Degree."""

    model = Degree
    template_name = "management/degree/degree_listview.html"
    context_object_name = "degrees"
    paginate_by = settings.PAGINATION["listview"]


class DegreeDetailView(DetailView):
    """DetailView for Degree."""

    model = Degree
    template_name = "management/degree/degree_detailview.html"
    context_object_name = "degree"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ratings"] = StudentRating.objects.filter(degree=self.object)

        if not groups_utils.is_manager_or_administrator(self.request.user):
            context["ratings"] = context["ratings"].filter(is_visible=True)

        return context


class DegreeCreateView(LoginRequiredMixin, ManagerAdministratorOnlyMixin,
                       BackOfficeResourceCreateViewMixin):
    """CreateView for Degree."""

    model = Degree
    form_class = DegreeCreateForm
    template_name = "management/degree/degree_createview.html"

    def get_context_data(self, **kwargs):
        """Add all DegreeCategory to context for select input."""

        context = super().get_context_data(**kwargs)
        context["categories"] = DegreeCategory.objects.all()
        return context

    def get_success_url(self):
        """Redirect to the update view of the created degree in order to add
        modules to it."""

        return reverse_lazy('degree_updateview', kwargs={'pk': self.object.id})


class DegreeUpdateView(LoginRequiredMixin, ManagerAdministratorOnlyMixin,
                       BackOfficeResourceUpdateViewMixin):
    """UpdateView for Degree."""

    model = Degree
    form_class = DegreeUpdateForm
    context_object_name = "degree"
    template_name = "management/degree/degree_updateview.html"

    def get_context_data(self, **kwargs):
        """Add all DegreeCategory and Module to context for select input."""

        context = super().get_context_data(**kwargs)
        context["categories"] = DegreeCategory.objects.all()
        context["modules"] = Module.objects.all()

        return context


class DegreeDeleteView(LoginRequiredMixin, ManagerAdministratorOnlyMixin,
                       DeleteView):
    """DeleteView for Degree."""

    model = Degree
    template_name = "management/degree/degree_deleteview.html"
    context_object_name = "degree"
    success_url = reverse_lazy('degree_listview')


# DegreeCategory

class DegreeCategoryListView(ListView):
    """ListView for DegreeCategory."""

    model = DegreeCategory
    template_name = "management/degree/degreecategory_listview.html"
    context_object_name = "categories"
    paginate_by = settings.PAGINATION["listview"]


class DegreeCategoryDetailView(DetailView):
    """DetailView for DegreeCategory."""

    model = DegreeCategory
    template_name = "management/degree/degreecategory_detailview.html"
    context_object_name = "category"


class DegreeCategoryCreateView(
    LoginRequiredMixin,
    ManagerAdministratorOnlyMixin,
    BackOfficeResourceCreateViewMixin,
):
    """CreateView for DegreeCategory."""

    model = DegreeCategory
    form_class = DegreeCategoryForm
    template_name = "management/degree/degreecategory_createview.html"

    def get_success_url(self):
        """Redirect the user to the newly created DegreeCategoryDetailView."""

        return reverse('degreecategory_detailview',
                       kwargs={"pk": self.object.pk})


class DegreeCategoryUpdateView(
    LoginRequiredMixin,
    ManagerAdministratorOnlyMixin,
    BackOfficeResourceUpdateViewMixin,
):
    """UpdateView for DegreeCategory."""

    model = DegreeCategory
    form_class = DegreeCategoryForm
    context_object_name = "category"
    template_name = "management/degree/degreecategory_updateview.html"


class DegreeCategoryDeleteView(LoginRequiredMixin,
                               ManagerAdministratorOnlyMixin, DeleteView):
    """DeleteView for DegreeCategory."""

    model = DegreeCategory
    template_name = "management/degree/degreecategory_deleteview.html"
    context_object_name = "category"
    success_url = reverse_lazy('degreecategory_listview')
