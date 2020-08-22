from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import Q

from ..models import ModuleRegistrationReport
from . import groups as groups_utils


def module_already_validated_by_user(user, module):
    """Check if a module has already been validated by a user."""

    return groups_utils.is_student(user) \
        and ModuleRegistrationReport.objects.filter(
        Q(student_rr__created_by=user),
        Q(module=module),
        (Q(status="EXEMPTED") | Q(status="COMPLETED")),
        Q(final_score__gte=settings.SUCCESS_SCORE_THRESHOLD)
    ).exists()


def all_prerequisites_validated_by_user(user, module):
    """Check if all the prerequisites modules has already been validated by the
    user."""

    all_prerequisites_validated = True

    for prerequisite in module.prerequisites.all():
        if not module_already_validated_by_user(user, prerequisite):
            all_prerequisites_validated = False
            break

    return groups_utils.is_student(user) and all_prerequisites_validated
