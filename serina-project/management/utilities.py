from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

from registration.utilities.groups_utils import is_member_of_promoted_group


def member_from_promoted_group_validation(user):
    """Check if a user is part of a promoted group and raise an error
    otherwise.

    The promoted groups are 'Professor', 'Manager' and 'Administrator'.
    """

    if not is_member_of_promoted_group(user):
        raise ValidationError(
            _("{} is not allowed to perform back-office tasks like this. "
              "These action must be performed by a promoted user."
              .format(user.username))
        )
