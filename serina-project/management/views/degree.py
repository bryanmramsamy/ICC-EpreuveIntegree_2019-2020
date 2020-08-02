from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import DeleteView, DetailView, ListView

from ..forms import DegreeCreateForm, DegreeCategoryForm, DegreeUpdateForm
from ..models import Degree, DegreeCategory
from .resource import (
    BackOfficeResourceCreateViewMixin,
    BackOfficeResourceUpdateViewMixin,
)


# Degree

class DegreeListView(ListView):  # TODO: Debug view
    """ListView for Degree."""

    model = Degree
    template_name = "management/degree/degree_listview.html"
    context_object_name = "degrees"
    paginate_by = 10


class DegreeDetailView(DetailView):  # TODO: Debug view
    """DetailView for Degree."""

    model = Degree
    template_name = "management/degree/degree_detailview.html"
    context_object_name = "degree"


class DegreeCreateView(BackOfficeResourceCreateViewMixin):  # TODO: Debug view
    """CreateView for Degree."""

    model = Degree
    form_class = DegreeCreateForm
    template_name = "management/degree/degree_createview.html"
    success_url = reverse_lazy('degree_listview')


class DegreeUpdateView(BackOfficeResourceUpdateViewMixin):  # TODO: Debug view
    """UpdateView for Degree."""

    model = Degree
    form_class = DegreeUpdateForm
    template_name = "management/degree/degree_updateview.html"

    def get_success_url(self):
        """Redirect the user to the newly created DegreeDetailView."""

        return reverse('degree_detailview', kwargs={"pk": self.object.pk})


class DegreeDeleteView(DeleteView):  # TODO: Debug view
    """DeleteView for Degree."""

    model = Degree
    template_name = "management/degree/degree_deleteview.html"
    context_object_name = "degree"
    success_url = reverse_lazy('degree_listview')


# DegreeCategory

class DegreeCategoryListView(ListView):  # TODO: Debug view
    """ListView for DegreeCategory."""

    model = DegreeCategory
    template_name = "management/degree/degreecategory_listview.html"
    context_object_name = "categories"
    paginate_by = 10


class DegreeCategoryDetailView(DetailView):  # TODO: Debug view
    """DetailView for DegreeCategory."""

    model = DegreeCategory
    template_name = "management/degree/degreecategory_detailview.html"
    context_object_name = "category"


class DegreeCategoryCreateView(BackOfficeResourceCreateViewMixin):  # TODO: Debug view
    """CreateView for DegreeCategory."""

    model = DegreeCategory
    form_class = DegreeCategoryForm
    template_name = "management/degree/degreecategory_createview.html"

    def get_success_url(self):
        """Redirect the user to the newly created DegreeCategoryDetailView."""

        return reverse('degreecategory_detailview',
                       kwargs={"pk": self.object.pk})


class DegreeCategoryUpdateView(BackOfficeResourceUpdateViewMixin):  # TODO: Debug view
    """UpdateView for DegreeCategory."""

    model = DegreeCategory
    form_class = DegreeCategoryForm
    context_object_name = "category"
    template_name = "management/degree/degreecategory_updateview.html"


class DegreeCategoryDeleteView(DeleteView):  # TODO: Debug view
    """DeleteView for DegreeCategory."""

    model = DegreeCategory
    template_name = "management/degree/degreecategory_deleteview.html"
    context_object_name = "category"
    success_url = reverse_lazy('degreecategory_listview')
