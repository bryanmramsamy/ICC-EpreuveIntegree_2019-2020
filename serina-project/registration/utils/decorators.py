from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

from . import groups as groups_utils
from . import messages as messages_utils


# Access control

def guests_only(function):  # TODO: DRY
    """Restrict a function access to the 'Guest'-group members only."""

    def wrapper(request, *args, **kwargs):
        """guests_only main wrapper."""

        if groups_utils.is_guest(request.user):
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrapper


def managers_or_administrators_only(function):  # TODO: DRY
    """Restrict a function access to managers or administrators only."""

    def wrapper(request, *args, **kwargs):
        """managers_or_administrators_only main wrapper."""

        if groups_utils.is_manager_or_administrator(request.user):
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrapper
