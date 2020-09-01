import graphene

from django.db.models import Q
from graphene_django import DjangoObjectType

from management.models import *
from rating.models import *
from registration.models import *
from registration.utils import management as management_utils


# Graphene object declaration

class ModuleType(DjangoObjectType):
    """Django Object Type definition for Module."""

    class Meta:
        """Meta definition for ModuleType."""

        model = Module


class CourseType(DjangoObjectType):
    """Django Object Type definition for Course."""

    status = graphene.String()

    class Meta:
        """Meta definition for CourseType."""

        model = Course


class ManagementStatsType(graphene.ObjectType):
    """Graphene value declarations for management statistic data."""

    total_modules = graphene.Int()
    total_module_levels = graphene.Int()
    total_degrees = graphene.Int()
    total_degrees_categories = graphene.Int()
    total_courses = graphene.Int()
    total_active_courses = graphene.Int()
    total_classrooms = graphene.Int()


# Root queries

class Query(graphene.ObjectType):
    """Root queries definitions."""

    modules = graphene.List(ModuleType)
    courses = graphene.List(CourseType)

    management_statistics = graphene.Field(ManagementStatsType)

    def resolve_modules(self, info):
        """Resolver for 'modules' query"""

        return Module.objects.all()

    def resolve_courses(self, info):
        """Resolver for 'courses' query"""

        return Course.objects.all()

    def resolve_management_statistics(self, info):
        """Resolver for 'managementStatistics' query"""

        return ManagementStatsType(
            total_modules=Module.objects.all().count(),
            total_module_levels=ModuleLevel.objects.all().count(),
            total_degrees=Degree.objects.all().count(),
            total_degrees_categories=DegreeCategory.objects.all().count(),
            total_courses=Course.objects.all().count(),
            total_active_courses=management_utils.count_active_courses(),
            total_classrooms=Classroom.objects.all().count()
        )

# Schema

schema = graphene.Schema(query=Query)
