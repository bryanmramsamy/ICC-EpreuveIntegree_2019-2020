from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import Q

from ..models import DegreeRegistrationReport, ModuleRegistrationReport
from . import groups as groups_utils


# Module Registration Reports

def module_still_ongoing_by_user(user, module):
    """Check if a module is still followed by the user."""

    return groups_utils.is_student(user) \
        and ModuleRegistrationReport.objects.filter(
        Q(student_rr__created_by=user),
        Q(module=module),
        (Q(status="APPROVED") | Q(status="PAYED"))
    ).exists()


def succeeded_module_rr_already_exists(user, module):
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
        if not succeeded_module_rr_already_exists(user, prerequisite):
            all_prerequisites_validated = False
            break

    return groups_utils.is_student(user) and all_prerequisites_validated


def active_module_rr_already_exists(user, module):
    """Check if a still active Module Registration Report exists for the given
    Student Registration Report.

    A still active Module Registration has either a 'PENDING', 'APPROVED' or
    'PAYED' status.
    """

    return groups_utils.is_student(user) and \
        ModuleRegistrationReport.objects.filter(
            Q(student_rr=user.student_rr),
            Q(module=module),
            Q(Q(status="PENDING") | Q(status="APPROVED") | Q(status="PAYED")),
        ).exists()


# Degree Registration Reports

def degree_still_ongoing_by_user(user, degree):
    """Check if a degree is still followed by the user."""

    return DegreeRegistrationReport.objects.filter(
        Q(student_rr__created_by=user),
        Q(degree=degree),
    ).exists()


def degree_already_validated_by_user(user, degree):
    """Check if a degree has already been completed by a user."""

    degrees_rrs = DegreeRegistrationReport.objects.filter(
        Q(student_rr__created_by=user),
        Q(degree=degree),
    )

    student_graduated = False
    for degree_rr in degrees_rrs:
        if degree_rr.student_graduated:
            student_graduated = True
            break

    return student_graduated
