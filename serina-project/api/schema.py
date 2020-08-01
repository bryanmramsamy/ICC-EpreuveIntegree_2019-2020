import graphene

from graphene_django import DjangoObjectType

from management.models import *
from rating.models import *
from registration.models import *


class ModulesType(DjangoObjectType):
    class Meta:
        model = Module


class Query(graphene.ObjectType):
    modules = graphene.List(ModulesType)
    nb_modules = graphene.Int()

    def resolve_modules(self, info):
        return Module.objects.all()

    def resolve_nb_modules(self, info):
        return Module.objects.all().count()  # FIXME: Incorrect syntax


schema = graphene.Schema(query=Query)
