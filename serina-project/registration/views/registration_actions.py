from django.contrib.auth.models import Group, User
from django.core.exceptions import PermissionDenied, ValidationError
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import ugettext as _

from ..forms import SubmitFinalScoreForm, SubmitNotesForm
from ..models import DegreeRegistrationReport, ModuleRegistrationReport
from ..utils import (
    decorators as decorators_utils,
    groups as groups_utils,
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

    if request.GET['admin'] == "true":
        return redirect('backoffice_user_admin_panel')
    else:
        return redirect('userprofile_detailview', pk=user.pk)


def administrator_on_admnistrator_only(request_user, updated_user):
    """Prevent an action performed on an administrator account by anyone else
    than another administrator."""

    if groups_utils.is_administrator(updated_user) \
       and not groups_utils.is_administrator(request_user):
        raise PermissionDenied


# @decorators_utils.managers_or_administrators_only
# def promote_to_guest(request, user_pk):
#     """Promote a registered user to the 'Guest'-group."""

#     user = get_object_or_404(User, pk=user_pk)
#     administrator_on_admnistrator_only(request.user, user)

#     groups_utils.promote_to_guest(user)
#     # TODO: Send mail
#     messages_utils.promote_to_guest(request, user)

#     return redirect('backoffice_user_admin_panel')


@decorators_utils.managers_or_administrators_only
def promote_to_group(request, group_name, user_pk):
    """Promote the given user to the given group.

    Only administrators can change the group of another administrator member.
    """

    user = get_object_or_404(User, pk=user_pk)
    administrator_on_admnistrator_only(request.user, user)
    group_name = group_name.capitalize()

    if group_name == "Guest" or group_name == "Student" \
       or group_name == "Teacher" or group_name == "Manager" \
       or group_name == "Administrator":
        group, is_created = Group.objects.get_or_create(name=group_name)
        group.save()

    if group.name == "Guest":
        groups_utils.promote_to_guest(user)

    elif group.name == "Student":
        try:
            groups_utils.promote_to_student(user)
        except Exception:
            messages_utils.cannot_promote_to_student_student_rr_missing(
                request,
                user,
            )

            return redirect('backoffice_user_admin_panel')

    elif group.name == "Teacher":
        groups_utils.promote_to_teacher(user)

    elif group.name == "Manager":
        groups_utils.promote_to_manager(user)

    elif group.name == "Administrator":
        groups_utils.promote_to_administrator(user)
    else:
        raise Exception("Group {} does not exist.".format(group_name))

    # TODO: Send mail
    messages_utils.promote_to_group(request, user, group)

    return redirect('backoffice_user_admin_panel')


# @decorators_utils.managers_or_administrators_only
# def promote_to_teacher(request, user_pk):
#     """Promote a registered user to the 'Teacher'-group."""

#     user = get_object_or_404(User, pk=user_pk)
#     administrator_on_admnistrator_only(request.user, user)

#     groups_utils.promote_to_teacher(user)
#     # TODO: Send mail
#     messages_utils.promote_to_teacher(request, user)

#     return redirect('backoffice_user_admin_panel')


# @decorators_utils.managers_or_administrators_only
# def promote_to_manager(request, user_pk):
#     """Promote a registered user to the 'Manager'-group."""

#     user = get_object_or_404(User, pk=user_pk)
#     administrator_on_admnistrator_only(request.user, user)

#     groups_utils.promote_to_manager(user)
#     # TODO: Send mail
#     messages_utils.promote_to_manager(request, user)

#     return redirect('backoffice_user_admin_panel')


# @decorators_utils.managers_or_administrators_only
# def promote_to_administrator(request, user_pk):
#     """Promote a registered user to the 'Administrator'-group."""

#     user = get_object_or_404(User, pk=user_pk)
#     administrator_on_admnistrator_only(request.user, user)

#     groups_utils.promote_to_administrator(user)
#     # TODO: Send mail
#     messages_utils.promote_to_administrator(request, user)

#     return redirect('backoffice_user_admin_panel')


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
