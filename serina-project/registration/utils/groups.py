from django.contrib.auth.models import Group
from django.db.models import Q
from django.utils.translation import ugettext as _


# Read utilities

def is_student(user):
    """Check if the user is a registered student."""

    return user.groups.filter(name="Student")


def is_back_office_user(user):
    """Check if the user is allowed to access the back office.

    The user must be member of one of the granted groups which are
    'Teacher', 'Manager', 'Administrator'.
    """

    return user.groups.filter(Q(name="Teacher")
                              | Q(name="Manager")
                              | Q(name="Administrator")).exists()


def is_manager_or_administrator(user):
    """Check if the user is member of the 'Manager'-group or the
    'Administrator'-group."""

    return user.groups.filter(Q(name="Manager")
                              | Q(name="Administrator")).exists()


def main_group_i18n(user):
    """Main group of the user in the case one has multiple groups.

    The group name is given with in its i18n version.
    """

    if user.groups.filter(name="Administrator").exists():
        main_group = _("Administrator")
    elif user.groups.filter(name="Manager").exists():
        main_group = _("Manager")
    elif user.groups.filter(name="Teacher").exists():
        main_group = _("Teacher")
    elif user.groups.filter(name="Student").exists():
        main_group = _("Student")
    else:
        main_group = _("Guest")

    return main_group


# Update utilities: Group alteration

def remove_from_all_groups(user):
    """Remove a user from all its groups.
    Remove the user access as staff member and superuser."""

    groups = Group.objects.all()

    for group in groups:
        group.user_set.remove(user)

    user.is_staff = False
    user.is_superuser = False


def add_to_group(user, group_name):
    """Add a user to a given group. Creates it if the group does not exist yet.
    """

    group, isCreated = Group.objects.get_or_create(name=group_name)
    group.user_set.add(user)

    return isCreated


def change_group(user, group_name):
    """Remove a user from all its group and add him/her to the given one."""

    remove_from_all_groups(user)
    add_to_group(user, group_name)


# Update utilities: Group promotion

def promote_to_guest(user):
    """Promote a registered user to the 'Guest'-group."""

    change_group(user, 'Guest')


def promote_to_student(user):
    """Promote a registered user to the 'Student'-group."""

    change_group(user, 'Student')


def promote_to_teacher(user):
    """Promote a registered user to the 'Teacher'-group."""

    change_group(user, 'Teacher')
    user.is_staff = True


def promote_to_manager(user):
    """Promote a registered user to the 'Manager'-group and make is staff
    member."""

    change_group(user, 'Manager')
    user.is_staff = True


def promote_to_administrator(user):
    """Promote a registered user to the 'Administrator'-group and make it
    superuser."""

    change_group(user, 'Administrator')
    user.is_staff = True
    user.is_superuser = True
