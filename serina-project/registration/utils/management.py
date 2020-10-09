from django.core.exceptions import PermissionDenied, ValidationError
from django.utils.translation import gettext_lazy as _

from ..models import ModuleRegistrationReport
from . import groups as groups_utils
from management.models import Course, Module


# Courses

def filter_active_courses():
    """Filter active courses based on their status."""

    active_courses = []

    for course in Course.objects.all():
        if course.status == "ONGOING":
            active_courses.append(course)

    return active_courses


def count_active_courses():
    """Count the amount of active courses."""

    return len(filter_active_courses())


def student_attends_course(user, course):
    """Template tags checking if the student is already attending the given
    course."""

    return groups_utils.is_student(user) \
        and course.modules_rrs.filter(student_rr__created_by=user).exists()


def student_module_rr_related_to_course(user, course):
    """Return the related Module Registration Report of the given course for
    the given user."""

    if not groups_utils.is_student(user):
        raise PermissionDenied

    else:
        return course.modules_rrs.all()


def still_registrable_courses(module):
    """Get the list of all the sill registrable courses based on the
    settings.COURSE_MINIMUM_REGISTRATION_DAYS value"""

    return [course for course in Course.objects.filter(module=module)
            if course.still_registrable]


def courses_sorted_by_attendance_percentage(courses):
    """Sort a list of courses by their attendance capacity.

    The attendance capacity is calculated by the percentage of free seats on
    the total amout of seats for a recommended capacity. If all the courses
    recommended capacity has been reached, the same calculation is made on the
    maximal capacity.
    """

    courses_by_recommended_attendance = sorted(
        courses,
        key=lambda course: course.recommended_attendance_percentage,
        reverse=False
    )

    if len(courses_by_recommended_attendance) == 0:
        raise ValidationError(_("No course was found for this module"))

    if courses_by_recommended_attendance[-1] \
       .recommended_attendance_percentage >= 1:
        courses_by_max_attendance = sorted(
            courses,
            key=lambda course: course.max_attendance_percentage,
            reverse=False
        )

        result_list = courses_by_max_attendance
    else:
        result_list = courses_by_recommended_attendance

    return result_list


def still_registrable_course_with_lowest_attendance(module):
    """Get the sill registrable courses with the lowest attendance capacity for
    the given module."""

    return courses_sorted_by_attendance_percentage(
        still_registrable_courses(module),
    )[0]


# ManyToMany relationship check

def is_eligible_teacher(teacher, module):
    """Check if the user is an eligible teacher of the given module."""

    return teacher.teachable_modules.filter(pk=module.pk).exists()


def is_prerequisite(potential_prerequisite, module):
    """Check if a module is a prerequisite of the other given module."""

    return potential_prerequisite.postrequisites.filter(pk=module.pk).exists()


def has_module(degree, module):
    """Check if a module is a prerequisite of the other given module."""

    return degree.modules.filter(pk=module.pk).exists()
