def modules_average_score(registration_report):
    """Compute the average score the student got for each of his/her module.

    If the student didn't followed a single module, the result will be -1.
    """

    sum_score = 0
    total_module = registration_report.modules_registration_reports\
        .count()

    if total_module > 0:
        for module_registration_report in registration_report\
                .modules_registration_reports.all():
            sum_score += module_registration_report.student_final_score

        return sum_score / total_module
    else:
        return -1
