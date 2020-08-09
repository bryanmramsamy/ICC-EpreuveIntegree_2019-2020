from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import ugettext as _

from ..forms import SubmitFinalScoreForm
from ..models import ModuleRegistrationReport
from ..utils import decorators as decorators_utils, messages as messages_utils

from management.models import Course


@decorators_utils.managers_or_administrators_only
def module_validation(request, pk):
    """Validate a ModuleRegistrationReport submitted based on its 'pk'.
    Register the student to the less populated course available for the chosen
    module. Also save the amount of attempts done by the student for the
    chosen module."""

    module_rr = get_object_or_404(ModuleRegistrationReport, pk=pk)
    if module_rr.approved:
        messages_utils.module_rr_already_approved(request)
    else:
        courses = Course.objects.filter(module=module_rr.module) \
                                .order_by("nb_registrants")

        if courses.count() == 0:
            messages_utils.module_rr_has_no_course(request, module_rr.module)
        else:
            selected_course = courses[0]
            selected_course.nb_registrants += 1
            selected_course.save()

            module_rr.nb_attempt = ModuleRegistrationReport.objects.filter(
                Q(student_rr=module_rr.student_rr) & Q(status="PAYED")).count()
            module_rr.course = selected_course
            module_rr.status = "APPROVED"
            module_rr.save()

            # TODO: Send mail to student
            messages_utils.module_rr_approved(request)

    return redirect(module_rr.get_absolute_url())


def module_score_submit(request, pk):
    """"""

    module_rr = get_object_or_404(ModuleRegistrationReport, pk=pk)

    if module_rr.status == "APPROVED" \
       or module_rr.status == "PAYED" \
       or module_rr.status == "EXEMPTED":
        form = SubmitFinalScoreForm(request.POST or None)

        if form.is_valid():
            score = form.cleaned_data['score']
            module_rr.final_score = score

            if module_rr.status == "PAYED":
                module_rr.status = "COMPLETED"

            module_rr.save()

        if module_rr.status == "APPROVED":
            messages_utils.module_rr_not_payed(request)
        else:
            messages_utils.module_rr_final_score_submitted(request)

    elif module_rr.status == "COMPLETED":
        messages_utils.module_rr_already_completed(request)
    else:
        messages_utils.module_rr_not_approved(request)

    return redirect(module_rr.get_absolute_url())
