from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import ugettext as _

from ..forms import SubmitFinalScoreForm, SubmitNotesForm
from ..models import DegreeRegistrationReport, ModuleRegistrationReport
from ..utils import (
    decorators as decorators_utils,
    management as management_utils,
    messages as messages_utils,
)

from management.models import Course


# User actions

@decorators_utils.managers_or_administrators_only
def activate_deactivate_user(request, user_pk):
    """Activate or deactivate a user."""

    user = get_object_or_404(User, pk=user_pk)

    if user.is_active:
        user.is_active = False

        # TODO: Send mail
        messages_utils.user_deactivated(request)
    else:
        user.is_active = True

        # TODO: Send mail
        messages_utils.user_activated(request)

    user.save()

    return redirect('userprofile_detailview', pk=user.pk)


# Module Registration Report actions

@decorators_utils.managers_or_administrators_only
def module_validation(request, pk):
    """Validate a ModuleRegistrationReport submitted based on its 'pk'.

    Register the student to the less populated course available for the chosen
    module. Also save the amount of attempts done by the student for the
    chosen module.
    """

    module_rr = get_object_or_404(ModuleRegistrationReport, pk=pk)
    if module_rr.approved:
        messages_utils.module_rr_already_approved(request)
    else:
        try:
            module_rr.course = management_utils. \
                still_registrable_course_with_lowest_attendance(
                    module_rr.module
                )

        except ValidationError:
            messages_utils.module_rr_has_no_course(request, module_rr.module)
            return redirect(module_rr.get_absolute_url())

        module_rr.nb_attempt = ModuleRegistrationReport.objects.filter(
            Q(student_rr=module_rr.student_rr),
            Q(status="COMPLETED"),
        ).count() + 1
        module_rr.status = "APPROVED"
        module_rr.save()

        # TODO: Send mail to student
        messages_utils.module_rr_approved(request)

    return redirect(module_rr.get_absolute_url())


@decorators_utils.managers_or_administrators_only
def module_deny(request, pk):
    """Denies a ModuleRegistrationReport submitted based on its 'pk'."""

    module_rr = get_object_or_404(ModuleRegistrationReport, pk=pk)

    if module_rr.approved:
        messages_utils.module_rr_already_approved(request)
    elif module_rr.status == "DENIED":
        messages_utils.module_rr_already_denied(request)
    else:
        module_rr.status = "DENIED"
        module_rr.save()

        # TODO: Send mail to student
        messages_utils.module_rr_denied(request)

    return redirect(module_rr.get_absolute_url())


def module_score_submit(request, pk):
    """Check if the module registration request has a valid status ('APPROVED',
    'PAYED' or 'EXEMPTED') in order to submit a final score to it."""

    module_rr = get_object_or_404(ModuleRegistrationReport, pk=pk)

    form_notes = SubmitNotesForm(request.POST or None)

    if form_notes.is_valid():
        module_rr.notes = form_notes.cleaned_data['notes']
        module_rr.save()

        messages_utils.module_rr_notes_updated(request)

        return redirect(module_rr.get_absolute_url())

    if not module_rr.status == "DENIED":
        form = SubmitFinalScoreForm(request.POST or None)

        if form.is_valid():
            module_rr.final_score = form.cleaned_data['final_score']

            if module_rr.status == "PAYED" and module_rr.final_score:
                module_rr.status = "COMPLETED"

            elif module_rr.status == "PENDING" and module_rr.final_score:
                module_rr.status = "EXEMPTED"

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


# Degree Registration Report actions

@decorators_utils.managers_or_administrators_only
def degree_validation(request, pk):
    """Validate a ModuleRegistrationReport submitted based on its 'pk'.

    Register the student to the less populated course available for the chosen
    module. Also save the amount of attempts done by the student for the
    chosen module.
    """

    pass  # TODO: Define action


@decorators_utils.managers_or_administrators_only
def degree_deny(request, pk):
    """Denies a ModuleRegistrationReport submitted based on its 'pk'."""

    pass  # TODO: Define action


def degree_notes_submit(request, pk):
    """Add note to degree report."""

    degree_rr = get_object_or_404(DegreeRegistrationReport, pk=pk)

    form_notes = SubmitNotesForm(request.POST or None)

    if form_notes.is_valid():
        degree_rr.notes = form_notes.cleaned_data['notes']
        degree_rr.save()

        messages_utils.module_rr_notes_updated(request)

        return redirect(degree_rr.get_absolute_url())
