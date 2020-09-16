from django import template
from django.contrib.auth.models import User

from ..models import Module
from registration.utils import management as management_utils

register = template.Library()


# Module select mutliple filters

@register.filter
def is_eligible_teacher(teacher, module):
    """Template tags checking if the user is an eligible teacher of the given
    module."""

    return management_utils.is_eligible_teacher(teacher, module)


@register.filter
def is_prerequisite(potential_prerequisite, module):
    """Template tags checking if the module is a prerequiste of another
    module."""

    return management_utils.is_prerequisite(potential_prerequisite, module)


# Degree select mutliple filters

@register.filter
def has_module(degree, module):
    """Template tags checking if the given module is part of the given
    degree."""

    return management_utils.has_module(degree, module)
