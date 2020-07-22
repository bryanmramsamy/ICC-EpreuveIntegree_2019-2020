from django.contrib.auth.models import Group, User
from django.db.models import Q


def username_generator(pk, date):
    """Generate a username registration number.

    The registration number has the (YYMMDDxxx) format with YY current year,
    MM the current month, DD the current day and xxx the pk given as argument
    filled with leading zeros.
    """

    return date.strftime("%y%m%d") + str(pk).zfill(3)


def username_exist(username):
    """Check if a username is already taken."""

    return User.objects.filter(username=username).exists()


def is_member_of_promoted_group(user):
    """Check if the user is a member of on of the promoted group.

    The promoted groups are: 'Professor', 'Manager', 'Administrator'
    """

    return user.groups.filter(Q(name="Professor") | Q(name="Manager")
                              | Q(name="Administrator")).exists()


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


def promote_to_guest(user):
    """Promote a registered user to the 'Guest'-group."""

    change_group(user, 'Guest')


def promote_to_student(user):
    """Promote a registered user to the 'Student'-group."""

    change_group(user, 'Student')


def promote_to_professor(user):
    """Promote a registered user to the 'Professor'-group."""

    change_group(user, 'Professor')


def promote_to_manager(user):
    """Promote a registered user to the 'Manager'-group and make is staff
    member."""

    change_group(user, 'Manager')
    user.is_staff = True


def promote_to_administrator(user):
    """Promote a registered user to the 'Administrator'-group and make it
    superuser."""

    change_group(user, 'Administrator')
    user.is_superuser = True
