from registration.models import *


def count_succeeded_modules():
    """Count the amount of succeeded modules based on their registration
    reports."""

    modules_rrs = ModuleRegistrationReport.objects.all()

    count_succeeded_modules = 0
    for module_rr in modules_rrs:
        if module_rr.succeeded:
            count_succeeded_modules += 1

    return count_succeeded_modules

def success_rate_modules():
    """Compute the success rate of all modules."""

    return (count_succeeded_modules()/ModuleRegistrationReport.objects.all() \
        .count())*100
