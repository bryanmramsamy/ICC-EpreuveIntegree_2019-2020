from django.views.generic import (
    CreateView,
)


class BackOfficeResourceCreateViewMixin(CreateView):
    """BackOfficeResourceEditViewMixin that populate the 'created_by' field by
    the current user."""

    def get_initial(self):
        """Returns the initial data to use for forms on this view."""

        initial = super().get_initial()
        initial['created_by'] = self.request.user
        return initial
