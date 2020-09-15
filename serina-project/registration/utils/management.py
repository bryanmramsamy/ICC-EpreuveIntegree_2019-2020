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


# ManyToMany relationship check

def is_eligible_teacher(teacher, module):
    """Check if the user is an eligible teacher of the given module."""

    return teacher.teachable_modules.filter(pk=module.pk).exists()


def is_prerequisite(potential_prerequisite, module):
    """Check if a module is a prerequisite of the other given module."""

    return potential_prerequisite.postrequisites.filter(pk=module.pk).exists()
