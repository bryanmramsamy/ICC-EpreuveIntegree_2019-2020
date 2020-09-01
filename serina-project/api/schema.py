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


class CountModulesStatType(graphene.ObjectType):
    count_modules = graphene.Int()


# Root queries

class Query(graphene.ObjectType):
    """Root queries definitions."""

    modules = graphene.List(ModulesType)
    count_modules = graphene.Field(CountModulesStatType)

    def resolve_modules(self, info):
        return Module.objects.all()

    def resolve_count_modules(self, info):
        return CountModulesStatType(
            count_modules=Module.objects.all().count()
        )


# Schema

schema = graphene.Schema(query=Query)
