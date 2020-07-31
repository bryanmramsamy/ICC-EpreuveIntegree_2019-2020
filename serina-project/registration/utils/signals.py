from django.contrib.auth.models import Group, User
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver

from . import groups, messages, users


@receiver(m2m_changed)
def user_promoted_from_guest_or_student(action, instance, model, **kwargs):
    """Change the user's username if the user is member of a promoted group.

    When a user has been promoted to a promoted group ('Teacher', 'Manager'
    or 'Administrator'), the user's username changes from the default unique
    registration number to the 'first_name.last_name' format.

    When the user is unpromoted from any promoted group, the username changes
    back to the default unique registration number based on the user's pk and
    the user's registration date.
    """

    if model == Group and action == 'post_add':
        old_username = instance.username
        if groups.is_back_office_user(instance):
            instance.username = "{}.{}".format(
                instance.first_name.lower(),
                instance.last_name.lower()
            )
            if users.username_already_exist(instance):
                instance.username += ".{}".format(instance.pk)
        else:
            instance.username = users.username_generator(
                instance.pk,
                instance.date_joined
            )
        new_username = instance.username

        print(old_username)
        print(new_username)

        # if old_username != new_username:
        #     messages.username_changed(old_username, new_username)  # FIXME: TypeError: username_changed() missing 1 required positional argument: 'new_username'

        # instance.save()
