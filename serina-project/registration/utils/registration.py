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

def degree_rr_is_completed(degree_rr):
    """Return True is at least on module registration report has been succeeded
    for each modules of the related degree of the given degree registration
    report.

    NOTE:
    A list booleans (module_succeeded_list) is parsed.
    One boolean for each module of the degree of the related degree
    registration report.

    If True, the module has at least one succeeded module registration report
    related to the given degree registration report.
    False if none of the modules registration reports, related to a module of
    the degree related to the given degree registration report, are succeeded.
    """

    module_succeeded_list = []
    for module in degree_rr.degree.modules.all():
        module_succeeded_list += [
            True in [module_rr.succeeded for module_rr
                     in module.modules_rrs.filter(degree_rr=degree_rr)]
        ]

    return False not in module_succeeded_list

# def get_degree_rr_status(degree_rr):  # FIXME: You motherfucking piece of shit
#     """Get the status of the Degree Registration Report.

#     The status is based on the statuses of all it's related Module Registration
#     Reports.
#     """

#     # Boolean check instanciation
#     degree_completed = True
#     degree_payed = True
#     degree_approved = True
#     degree_not_denied = True
#     degree_pending = True

#     # Loop for each module of the degree
#     for module in degree_rr.degree.modules.all():

#         # Get all module registrations related to this module only
#         module_related_modules_rrs = degree_rr.modules_rrs.filter(
#             module=module,
#         )  # NOTE: OK

#         # If not a single module registration was succeeded, the degree is not
#         # completed
#         if degree_completed and not (True in [
#             module_rr.succeeded for module_rr in module_related_modules_rrs
#         ]):
#             degree_completed = False  # NOTE: OK

#         # If not a single module registration has a 'PAYED' status, the degree
#         # is not payed
#         print([
#             not (True in [
#             (module_rr.payed_or_exempted and not module_rr.succeeded) for module_rr in module_related_modules_rrs
#         ])
#         ])
#         if degree_payed and not (True in [
#             (module_rr.payed_or_exempted and not module_rr.succeeded) for module_rr in module_related_modules_rrs
#         ]):
#             degree_payed = False

#     # Result degree registration status
#     if degree_completed:
#         return "COMPLETED"
#     elif degree_payed:
#         return "PAYED"



