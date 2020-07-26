from django.contrib.auth.models import User


def username_already_exist(user):
    """Check if a username is already taken."""

    return User.objects.exclude(pk=user.pk).filter(username=user.username) \
        .exists()


def username_generator(pk, date):
    """Generate a username registration number.

    The registration number has the (YYMMDDxxx) format with YY current year,
    MM the current month, DD the current day and xxx the pk given as argument
    filled with leading zeros.
    """

    return date.strftime("%y%m%d") + str(pk).zfill(3)
