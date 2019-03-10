import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models import db_session, Department as DepartmentModel


class DepartmentAttribute:
    name = graphene.String(description="Name of the department")


class DepartmentType(SQLAlchemyObjectType, DepartmentAttribute):
    class Meta:
        model = DepartmentModel
        interfaces = (relay.Node, )


class DepartmentConnection(relay.Connection):
    class Meta:
        node = DepartmentType


class Query(graphene.ObjectType):
    departments = SQLAlchemyConnectionField(DepartmentConnection)
