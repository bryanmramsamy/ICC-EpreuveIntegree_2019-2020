from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q


def back_office_member_only(user):
    """Requires user membership in at least one of the groups passed in."""

    def in_groups(user):
        if user.is_authenticated:
            if bool(user.groups.filter(Q(name="Manager")
                                       | Q(name="Administrator")).exists()):
                return True
        return False

    return user_passes_test(in_groups)

# def user_is_entry_author(function):
#     def wrap(request, *args, **kwargs):
#         entry = Entry.objects.get(pk=kwargs['entry_id'])
#         if entry.created_by == request.user:
#             return function(request, *args, **kwargs)
#         else:
#             raise PermissionDenied
#     wrap.__doc__ = function.__doc__
#     wrap.__name__ = function.__name__
#     return wrap