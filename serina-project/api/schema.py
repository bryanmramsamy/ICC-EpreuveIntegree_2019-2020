import graphene

from django.contrib.auth.models import User
from django.db.models import Avg, Q
from graphene_django import DjangoObjectType

from management.models import *
from rating.models import *
from registration.models import *
from registration.utils import management as management_utils


# Graphene types declaration

## Management

class ModuleType(DjangoObjectType):
    """Django Object Type definition for Module."""

    class Meta:
        """Meta definition for ModuleType."""

        model = Module


class ModuleLevelType(DjangoObjectType):
    """Django Object Type definition for ModuleLevel."""

    class Meta:
        """Meta definition for ModuleLevelType."""

        model = ModuleLevel


class DegreeType(DjangoObjectType):
    """Django Object Type definition for Degree."""

    class Meta:
        """Meta definition for DegreeType."""

        model = Degree


class DegreeCategoryType(DjangoObjectType):
    """Django Object Type definition for DegreeCategory."""

    class Meta:
        """Meta definition for DegreeCategoryType."""

        model = DegreeCategory


class CourseType(DjangoObjectType):
    """Django Object Type definition for Course."""

    status = graphene.String()

    class Meta:
        """Meta definition for CourseType."""

        model = Course


class ClassroomType(DjangoObjectType):
    """Django Object Type definition for Classroom."""

    class Meta:
        """Meta definition for ClassroomType."""

        model = Classroom


class ReferenceWhere(graphene.InputObjectType):
    """InputObjectType definition for any management object for filtering on
    reference."""

    reference = graphene.String()


class ManagementStatsType(graphene.ObjectType):
    """Graphene value declarations for management statistic data."""

    total_modules = graphene.Int()
    total_module_levels = graphene.Int()
    total_degrees = graphene.Int()
    total_degree_categories = graphene.Int()
    total_courses = graphene.Int()
    total_active_courses = graphene.Int()
    total_classrooms = graphene.Int()


## Registration

# class ClassroomType(DjangoObjectType):
#     """Django Object Type definition for Classroom."""

#     class Meta:
#         """Meta definition for ClassroomType."""

#         model = Classroom

class RegistrationStatsType(graphene.ObjectType):
    """Graphene value declarations for registration statistic data."""

    total_guests = graphene.Int()
    total_students = graphene.Int()
    total_teachers = graphene.Int()
    total_module_registration_reports = graphene.Int()
    total_module_registration_reports_without_degrees = graphene.Int()
    total_module_registration_reports_from_degrees = graphene.Int()
    total_degree_registration_reports = graphene.Int()


class ScoresStatsType(graphene.ObjectType):
    """Graphene value declarations for registration scores statistic data."""

    average_score_on_all_modules = graphene.Float()


# Root queries

class Query(graphene.ObjectType):
    """Root queries definitions."""

    module = graphene.NonNull(ModuleType, where=ReferenceWhere())
    modules = graphene.List(ModuleType)
    module_levels = graphene.List(ModuleLevelType)
    degree = graphene.NonNull(DegreeType, where=ReferenceWhere())
    degrees = graphene.List(DegreeType)
    degree_categories = graphene.List(DegreeCategoryType)
    course = graphene.NonNull(CourseType, where=ReferenceWhere())
    courses = graphene.List(CourseType)
    classroom = graphene.NonNull(ClassroomType, where=ReferenceWhere())
    classrooms = graphene.List(ClassroomType)

    management_statistics = graphene.Field(ManagementStatsType)

    registration_statistics = graphene.Field(RegistrationStatsType)

    scores_statistics = graphene.Field(ScoresStatsType)

    def resolve_module(self, info, where):
        """Resolver for 'module' query"""

        reference = where.get("reference")

        return Module.objects.get(reference__iexact=reference)

    def resolve_modules(self, info):
        """Resolver for 'modules' query"""

        return Module.objects.all()

    def resolve_module_levels(self, info):
        """Resolver for 'module_levels' query"""

        return ModuleLevel.objects.all()

    def resolve_degree(self, info, where):
        """Resolver for 'degree' query"""

        reference = where.get("reference")

        return Degree.objects.get(reference__iexact=reference)

    def resolve_degrees(self, info):
        """Resolver for 'degrees' query"""

        return Degree.objects.all()

    def resolve_degree_categories(self, info):
        """Resolver for 'degree_categories' query"""

        return DegreeCategory.objects.all()

    def resolve_course(self, info, where):
        """Resolver for 'course' query"""

        reference = where.get("reference")

        return Course.objects.get(reference__iexact=reference)

    def resolve_courses(self, info):
        """Resolver for 'courses' query"""

        return Course.objects.all()

    def resolve_classroom(self, info, where):
        """Resolver for 'classroom' query"""

        reference = where.get("reference")

        return Classroom.objects.get(reference__iexact=reference)

    def resolve_classrooms(self, info):
        """Resolver for 'classrooms' query"""

        return Classroom.objects.all()

    def resolve_management_statistics(self, info):
        """Resolver for 'managementStatistics' query"""

        return ManagementStatsType(
            total_modules=Module.objects.all().count(),
            total_module_levels=ModuleLevel.objects.all().count(),
            total_degrees=Degree.objects.all().count(),
            total_degree_categories=DegreeCategory.objects.all().count(),
            total_courses=Course.objects.all().count(),
            total_active_courses=management_utils.count_active_courses(),
            total_classrooms=Classroom.objects.all().count()
        )

    def resolve_registration_statistics(self, info):
        """Resolver for 'managementStatistics' query"""

        return RegistrationStatsType(
            total_guests=User.objects \
                .filter(groups__name__exact="Guest").count(),
            total_students=User.objects \
                .filter(groups__name__exact="Student").count(),
            total_teachers=User.objects \
                .filter(groups__name__exact="Teacher").count(),
            total_module_registration_reports = ModuleRegistrationReport \
                .objects.all().count(),
            total_module_registration_reports_without_degrees = \
                ModuleRegistrationReport.objects \
                .filter(degree_rr__isnull=True).count(),
            total_module_registration_reports_from_degrees = \
                ModuleRegistrationReport.objects \
                .filter(degree_rr__isnull=False).count(),
            total_degree_registration_reports = \
                DegreeRegistrationReport.objects.all().count(),
        )
    
    def resolve_scores_statistics(self, info):
        """Resolver for 'scoresStatistics' query"""

        return ScoresStatsType(
            average_score_on_all_modules = ModuleRegistrationReport.objects. \
                all().aggregate(Avg('final_score'))["final_score__avg"]
        )

# Schema

schema = graphene.Schema(query=Query)
