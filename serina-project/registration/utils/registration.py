from decimal import Decimal

from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import Max, Q

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


def get_all_succeeded_module_rr(user, module):
    """Get the list of all the Registration Reports for the given the module by
    the given user which were succeeded or exempted."""

    return ModuleRegistrationReport.objects.filter(
        Q(student_rr__created_by=user),
        Q(module=module),
        (Q(status="EXEMPTED") | Q(status="COMPLETED")),
        Q(final_score__gte=settings.SUCCESS_SCORE_THRESHOLD)
    )


def succeeded_module_rr_already_exists(user, module):
    """Check if a module has already been validated by a user."""

    return groups_utils.is_student(user) \
        and get_all_succeeded_module_rr(user, module).exists()


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

    return degree_rr.graduated if degree_rr else False


def create_modules_rrs_for_degree_rr(degree_rr):
    """Create all the Module Registration Reports for each module of the
    degree from the given Degree Registration Report.

    If a Module Registration Report already validated or exempted already
    exists for a specific module, a new report will be created and flagged as
    'EXEMPTED'. The final score will be repported as well.

    Returns the amount of modules registration that were exempted.
    """

    for module in degree_rr.degree.modules.all():

        module_rr = ModuleRegistrationReport(
            student_rr=degree_rr.student_rr,
            degree_rr=degree_rr,
            module=module,
        )

        modules_rrs = get_all_succeeded_module_rr(
            degree_rr.student_rr.created_by,
            module,
        )

        print("DEBUG: ", module, " -> ", modules_rrs.exists())

        if modules_rrs.exists():
            max_score_found = modules_rrs.aggregate(Max('final_score'))

            module_rr.final_score = max_score_found["final_score__max"]
            module_rr.status = "EXEMPTED"
            module_rr.notes = (
                "System generated message: Student already succeeded this "
                "module before. Maximum found final score was repported and "
                "module registration was flagged as exempted."
            )

        module_rr.save()


# Degree Registration Report statuses

def degree_rr_is_partially_pending(degree_rr):
    """True if at least on module registration report has been pending for each
    module of the related degree of the given degree registration report."""

    module_partially_pending_list = []
    for module in degree_rr.degree.modules.all():
        module_partially_pending_list += [
            not module.modules_rrs.filter(degree_rr=degree_rr)
                                  .exclude(status="PENDING")
                                  .exclude(status="EXEMPTED").exists()
        ]

    return True in module_partially_pending_list


def degree_rr_is_fully_pending(degree_rr):
    """True if all the module registration reports has been pending for each
    module of the related degree of the given degree registration report."""

    module_fully_pending_list = []
    for module in degree_rr.degree.modules.all():
        module_fully_pending_list += [
            not module.modules_rrs.filter(degree_rr=degree_rr)
                                  .exclude(status="PENDING")
                                  .exclude(status="EXEMPTED").exists()
        ]

    return False not in module_fully_pending_list


def degree_rr_is_partially_denied(degree_rr):
    """True if at least on module registration report has been denied for each
    module of the related degree of the given degree registration report."""

    module_partially_denied_list = []
    for module in degree_rr.degree.modules.all():
        module_partially_denied_list += [
            not module.modules_rrs.filter(degree_rr=degree_rr)
                                  .exclude(status="DENIED").exists()
        ]

    return True in module_partially_denied_list


def degree_rr_is_fully_denied(degree_rr):
    """True if all the module registration reports has been denied for each
    module of the related degree of the given degree registration report."""

    module_fully_denied_list = []
    for module in degree_rr.degree.modules.all():
        module_fully_denied_list += [
            not module.modules_rrs.filter(degree_rr=degree_rr)
                                  .exclude(status="DENIED").exists()
        ]

    return False not in module_fully_denied_list


def degree_rr_is_partially_approved(degree_rr):
    """True if at least on module registration report has been approved, payed
    or was completed or exempted for each module of the related degree of the
    given degree registration report."""

    module_partially_approved_list = []
    for module in degree_rr.degree.modules.all():
        module_partially_approved_list += [
            True in [module_rr.approved for module_rr
                     in module.modules_rrs.filter(degree_rr=degree_rr)
                     .exclude(status="EXEMPTED")]
        ]

    return True in module_partially_approved_list


def degree_rr_is_fully_approved(degree_rr):
    """True if all the module registration reports has been approved, payed or
    was completed or exempted for each module of the related degree of the
    given degree registration report."""

    module_fully_approved_list = []
    for module in degree_rr.degree.modules.all():
        module_fully_approved_list += [
            False not in [module_rr.approved for module_rr
                          in module.modules_rrs.filter(degree_rr=degree_rr)
                          .exclude(status="EXEMPTED")]
        ]

    return False not in module_fully_approved_list


def degree_rr_is_partially_payed(degree_rr):
    """True if at least on module registration report has been payed or
    was completed or exempted for each module of the related degree of the
    given degree registration report."""

    module_partially_paid_list = []
    for module in degree_rr.degree.modules.all():
        module_partially_paid_list += [
            True in [module_rr.payed for module_rr
                     in module.modules_rrs.filter(degree_rr=degree_rr)
                     .exclude(status="EXEMPTED")]
        ]

    return True in module_partially_paid_list


def degree_rr_is_fully_payed(degree_rr):
    """True if all the module registration reports has been payed or
    was completed or exempted for each module of the related degree of the
    given degree registration report."""

    module_fully_paid_list = []
    for module in degree_rr.degree.modules.all():
        module_fully_paid_list += [
            False not in [module_rr.payed for module_rr
                          in module.modules_rrs.filter(degree_rr=degree_rr)
                          .exclude(status="EXEMPTED")]
        ]

    return False not in module_fully_paid_list


def degree_rr_is_completed(degree_rr):
    """True if at least on module registration report has been succeeded
    for each module of the related degree of the given degree registration
    report."""

    module_succeeded_list = []
    for module in degree_rr.degree.modules.all():
        module_succeeded_list += [
            True in [module_rr.succeeded for module_rr
                     in module.modules_rrs.filter(degree_rr=degree_rr)]
        ]

    return False not in module_succeeded_list
