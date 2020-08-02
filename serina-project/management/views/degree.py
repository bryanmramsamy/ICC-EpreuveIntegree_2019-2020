from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import DeleteView, DetailView, ListView

from ..forms import DegreeCreateForm, DegreeCategoryForm, DegreeUpdateForm
from ..models import Degree, DegreeCategory
from .resource import (
    BackOfficeResourceCreateViewMixin,
    BackOfficeResourceUpdateViewMixin,
)
from registration.utils.mixins import ManagerAdministratorOnlyMixin


# Degree

class DegreeListView(LoginRequiredMixin, ManagerAdministratorOnlyMixin,
                     ListView):  # TODO: Debug view
    """ListView for Degree."""

    model = Degree
    template_name = "management/degree/degree_listview.html"
    context_object_name = "degrees"
    paginate_by = 10


class DegreeDetailView(LoginRequiredMixin, ManagerAdministratorOnlyMixin,
                       DetailView):  # TODO: Debug view
    """DetailView for Degree."""

    model = Degree
    template_name = "management/degree/degree_detailview.html"
    context_object_name = "degree"


class DegreeCreateView(LoginRequiredMixin, ManagerAdministratorOnlyMixin,
                       BackOfficeResourceCreateViewMixin):  # TODO: Debug view
    """CreateView for Degree."""

    model = Degree
    form_class = DegreeCreateForm
    template_name = "management/degree/degree_createview.html"
    success_url = reverse_lazy('degree_listview')


class DegreeUpdateView(LoginRequiredMixin, ManagerAdministratorOnlyMixin,
                       BackOfficeResourceUpdateViewMixin):  # TODO: Debug view
    """UpdateView for Degree."""

    model = Degree
    form_class = DegreeUpdateForm
    template_name = "management/degree/degree_updateview.html"

    def get_success_url(self):
        """Redirect the user to the newly created DegreeDetailView."""

        return reverse('degree_detailview', kwargs={"pk": self.object.pk})


class DegreeDeleteView(LoginRequiredMixin, ManagerAdministratorOnlyMixin,
                       DeleteView):  # TODO: Debug view
    """DeleteView for Degree."""

    model = Degree
    template_name = "management/degree/degree_deleteview.html"
    context_object_name = "degree"
    success_url = reverse_lazy('degree_listview')


# DegreeCategory

class DegreeCategoryListView(LoginRequiredMixin, ManagerAdministratorOnlyMixin,
                             ListView):  # TODO: Debug view
    """ListView for DegreeCategory."""

    model = DegreeCategory
    template_name = "management/degree/degreecategory_listview.html"
    context_object_name = "categories"
    paginate_by = 10


class DegreeCategoryDetailView(LoginRequiredMixin,
                               ManagerAdministratorOnlyMixin, DetailView):  # TODO: Debug view
    """DetailView for DegreeCategory."""

    model = DegreeCategory
    template_name = "management/degree/degreecategory_detailview.html"
    context_object_name = "category"


class DegreeCategoryCreateView(
    LoginRequiredMixin,
    ManagerAdministratorOnlyMixin,
    BackOfficeResourceCreateViewMixin,
):  # TODO: Debug view
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
):  # TODO: Debug view
    """UpdateView for DegreeCategory."""

    model = DegreeCategory
    form_class = DegreeCategoryForm
    context_object_name = "category"
    template_name = "management/degree/degreecategory_updateview.html"


class DegreeCategoryDeleteView(LoginRequiredMixin,
                               ManagerAdministratorOnlyMixin, DeleteView):  # TODO: Debug view
    """DeleteView for DegreeCategory."""

    model = DegreeCategory
    template_name = "management/degree/degreecategory_deleteview.html"
    context_object_name = "category"
    success_url = reverse_lazy('degreecategory_listview')
