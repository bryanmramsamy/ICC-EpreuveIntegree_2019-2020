from django.contrib.auth.models import Group, User
from django.db.models import Q
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver

from . import group_management


@receiver(m2m_changed)
def user_promoted_from_guest_or_student(action, instance, model, **kwargs):
    """Change the user's username if the user is member of a promoted group.

    When a user has been promoted to a promoted group ('Professor', 'Manager'
    or 'Administrator'), the user's username changes from the default unique
    registration number to the 'first_name.last_name' format.

    When the user is unpromoted from any promoted group, the username changes
    back to the default unique registration number based on the user's pk and
    the user's registration date.
    """

    if model == Group and action == 'post_add':
        if instance.groups.filter(Q(name="Professor")
                                  | Q(name="Manager")
                                  | Q(name="Administrator")).exists():
            instance.username = instance.first_name + instance.last_name
        else:
            instance.username = group_management.username_generator(
                instance.pk,
                instance.date_joined
            )

        instance.save()
