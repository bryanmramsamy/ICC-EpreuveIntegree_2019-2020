from django import template
from django.contrib.auth.models import Group

from ..utils import (
    groups as groups_utils,
    management as management_utils,
    registration as registration_utils,
)


register = template.Library()


# Group authorizations

@register.filter
def is_guest(user):
    """Template tags checking if the user is part of the 'Guest'-group."""

    return groups_utils.is_guest(user)


@register.filter
def is_student(user):
    """Template tags that checks if a user is a student or not."""

    return groups_utils.is_student(user)


@register.filter
def is_back_office_user(user):
    """Template tags that checks if a user is a back-office user or not.

    Back-Office users are users from either the 'Teacher', the 'Manager' or the
    'Administrator' group."""

    return groups_utils.is_back_office_user(user)


@register.filter
def is_teacher(user):
    """Template tags that checks if a user is a teacher or not."""

    return groups_utils.is_teacher(user)


@register.filter
def is_manager_or_administrator(user):
    """Template tags that checks if a user is is manager or administrator."""

    return groups_utils.is_manager_or_administrator(user)


# Module Registration Report


@register.filter
def active_module_rr_already_exists(user, module):
    """Filter that checks if the user is still following the given module."""

    return registration_utils.active_module_rr_already_exists(user, module)


@register.filter
def succeeded_module_rr_already_exists(user, module):
    """Filter that checks if the user has already vaidated the given module."""

    return registration_utils.succeeded_module_rr_already_exists(user, module)


@register.filter
def all_prerequisites_validated_by_user(user, module):
    """Filter that checks if the user has already vaidated the prerequisites
    for the given module."""

    return registration_utils.all_prerequisites_validated_by_user(user, module)


# Degree Registration Report

@register.filter
def active_degree_rr_already_exists(user, degree):
    """Filter that checks if the given user was has a pending or validated
    registration for the given degree."""

    return registration_utils.active_degree_rr_already_exists(user, degree)


@register.filter
def succeeded_degree_rr_already_exists(user, degree):
    """Filter that checks if the user has already validated the given
    degree."""

    return registration_utils.succeeded_degree_rr_already_exists(user, degree)


# Course

@register.filter
def attends_course(user, course):
    """Template tags checking if the student is already attending the given
    course."""

    return management_utils.student_attends_course(user, course)
