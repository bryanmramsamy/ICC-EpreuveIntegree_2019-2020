from django import template
from django.contrib.auth.models import Group

from ..utils import groups as groups_utils


register = template.Library()


@register.filter
def is_student(user):
    """Template tags that checks if a user is a student or not."""

    return groups_utils.is_student(user)


@register.filter
def is_manager_or_administrator(user):
    """Template tags that checks if a user is is manager or administrator."""

    return groups_utils.is_manager_or_administrator(user)


# @register.filter(takes_context=True)
# def user_is_student(context):
#     """Template tags that checks if a user is a student or not."""

#     request = context.get("request")
#     return groups_utils.is_student(request.user)
