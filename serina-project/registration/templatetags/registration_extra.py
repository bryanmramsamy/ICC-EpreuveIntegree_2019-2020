from django import template
from django.contrib.auth.models import Group

from ..utils import groups as groups_utils, registration as registration_utils


register = template.Library()


# Group authorizations

@register.filter
def is_student(user):
    """Template tags that checks if a user is a student or not."""

    return groups_utils.is_student(user)


@register.filter
def is_manager_or_administrator(user):
    """Template tags that checks if a user is is manager or administrator."""

    return groups_utils.is_manager_or_administrator(user)


# Module Registration Report

@register.filter
def module_already_validated_by_user(user, module):
    """Filter that checks if the user has already vaidated the given module."""

    return registration_utils.module_already_validated_by_user(user, module)


@register.filter
def all_prerequisites_validated_by_user(user, module):
    """Filter that checks if the user has already vaidated the prerequisites
    for the given module."""

    return registration_utils.all_prerequisites_validated_by_user(user, module)


# Degree Registration Report

@register.filter
def degree_already_validated_by_user(user, degree):
    """Filter that checks if the user has already vaidated the given degree."""

    return registration_utils.degree_already_validated_by_user(user, degree)
