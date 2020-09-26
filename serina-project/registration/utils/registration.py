from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import Q

from ..models import DegreeRegistrationReport, ModuleRegistrationReport
from . import groups as groups_utils


# Module Registration Reports

def active_module_rr_already_exists(user, module):
    """Check if a still active Module Registration Report exists for the given
    Student Registration Report.

    A still active Module Registration has either a 'PENDING', 'APPROVED' or
    'PAYED' status.
    """

    return groups_utils.is_student(user) \
        and ModuleRegistrationReport.objects.filter(
        Q(student_rr__created_by=user),
        Q(module=module),
        Q(Q(status="PENDING") | Q(status="APPROVED") | Q(status="PAYED")),
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


# Degree Registration Reports

def get_degree_rr_from_user_and_degree(user, degree):
    """Get the unique Degree Registration Report from the given user for the
    given degree.

    Return 'None' if the report does not exists.
    """

    degree_rr = DegreeRegistrationReport.objects.filter(
        Q(student_rr__created_by=user),
        Q(degree=degree),
    )

    if degree_rr.count() > 1:
        raise Exception("Mutliple DegreeRegistrationReports objects found for "
                        "degree: {} for user: {}".format(degree, user))

    if degree_rr.exists():
        return degree_rr.get()
    else:
        return None


def pending_degree_rr_already_exists(user, degree):
    """Check if the given user has his/her degree subscribtion still
    pending."""

    degree_rr = get_degree_rr_from_user_and_degree(user, degree)

    return degree_rr.partially_pending if degree_rr else False


def active_degree_rr_already_exists(user, degree):
    """Check if a degree is still followed by the user."""

    degree_rr = get_degree_rr_from_user_and_degree(user, degree)

    return ((degree_rr.partially_approved and degree_rr.partially_denied)
            or degree_rr.fully_approved
            or pending_degree_rr_already_exists(user, degree)) \
        if degree_rr else False


def succeeded_degree_rr_already_exists(user, degree):
    """Check if a degree has already been completed by a user."""

    degree_rr = get_degree_rr_from_user_and_degree(user, degree)

    return degree_rr.student_graduated if degree_rr else False
