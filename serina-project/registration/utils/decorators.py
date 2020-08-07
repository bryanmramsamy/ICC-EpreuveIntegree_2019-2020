from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from django.shortcuts import redirect

from . import groups as groups_utils
from . import messages as messages_utils


def managers_or_administrators_only(function):
    """Restrict a function acces to managers or administrators only."""

    def wrapper(request, *args, **kwargs):
        """managers_or_administrators_only main wrapper."""

        if groups_utils.is_manager_or_administrator(request.user):
            return function(request, *args, **kwargs)
        else:
            messages_utils.permission_denied(request)
            return redirect("home")

    return wrapper
