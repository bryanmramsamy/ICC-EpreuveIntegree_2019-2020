from django.shortcuts import render
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
)

from ..forms import ModuleForm, ModuleLevelForm
from ..models import Module, ModuleLevel


# Module views

class ModuleListView(ListView):  # TODO: Debug view
    """ListView for Modules."""

    model = Module
    template_name = "management/module_listview.html"
    context_object_name = "modules"
    paginate_by = 10


class ModuleDetailView(DetailView):  # TODO: Debug view
    """DetailView for Modules."""

    model = Module
    template_name = "management/module_detailview.html"
    context_object_name = "module"


class ModuleCreateView(CreateView):
    """CreateView for Modules."""

    model = Module
    form_class = ModuleForm
    template_name = "management/module_createview.html"


# ModuleLevel Views

class ModuleLevelListView(ListView):  # TODO: Debug view
    """ListView for ModuleLevels."""

    model = ModuleLevel
    template_name = "management/modulelevel_listview.html"
    context_object_name = "levels"


class ModuleLevelDetailView(DetailView):  # TODO: Debug view
    """DetailView for ModuleLevels."""

    model = ModuleLevel
    template_name = "management/modulelevel_detailview.html"
    context_object_name = "level"


class ModuleLevelCreateView(CreateView):
    # FIXME: Doesn't add object to database
    """CreateView for ModuleLevels."""

    model = ModuleLevel
    form_class = ModuleLevelForm
    template_name = "management/modulelevel_createview.html"

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        initial = super().get_initial()

        initial['created_by'] = self.request.user

        return initial


    # def form_valid(self, form):
    #     """If the form is valid, save the associated model."""
    #     self.object = form.save()
    #     return super().form_valid(form)
        
    #     """If the form is valid, redirect to the supplied URL."""
    #     return HttpResponseRedirect(self.get_success_url())


    # def form_valid(self, form):
    #     model = form.save(commit=False)
    #     model.created_by = self.request.user
    #     model.save()
    #     return super(ModuleLevelCreateView, self).form_valid(form)

    # def form_valid(self, form):
    #     """If the form is valid, save the associated model."""

    #     self.object = form.save(commit=False)
    #     self.object.created_by = self.request.user
    #     return super().form_valid(form)

    # def post(self, request, *args, **kwargs):
    #     form = ModuleLevelForm(request.POST)
    #     form.created_by = self.request.user

    #     if form.is_valid():
    #         book = form.save()
    #         book.save()
    #     #     return HttpResponseRedirect(reverse_lazy('books:detail', args=[book.id]))
    #     # return render(request, 'books/book-create.html', {'form': form})

    #     return super().post(request, *args, **kwargs)
