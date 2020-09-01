import graphene

from graphene_django import DjangoObjectType

from management.models import *
from rating.models import *
from registration.models import *


# Graphene object declaration

class ModulesType(DjangoObjectType):
    """Django Object Type definition for Module."""

    class Meta:
        """Meta definition for ModulesType."""

        model = Module


class ManagementStatsType(graphene.ObjectType):
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

    modules = graphene.List(ModulesType)

    management_statistics = graphene.Field(ManagementStatsType)

    def resolve_modules(self, info):
        return Module.objects.all()

    def resolve_management_statistics(self, info):
        return ManagementStatsType(
            total_modules=Module.objects.all().count(),
            total_module_levels=ModuleLevel.objects.all().count(),
            total_degrees=Degree.objects.all().count(),
            total_degrees_categories=DegreeCategory.objects.all().count(),
            total_courses=Course.objects.all().count(),
            total_active_courses=Course.objects.all().count(),  # TODO: Must be filtered
            total_classrooms=Classroom.objects.all().count()
        )

# Schema

schema = graphene.Schema(query=Query)
