from management.models import Course


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
