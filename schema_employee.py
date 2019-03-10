import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models import db_session, Employee as EmployeeModel
import utils


class EmployeeAttribute:
    name = graphene.String(description="Name of the employee")
    departmentId = graphene.String(description="ID of the department to which the employee belongs")


class EmployeeType(SQLAlchemyObjectType, EmployeeAttribute):
    class Meta:
        model = EmployeeModel
        interfaces = (relay.Node, )


class EmployeeConnection(relay.Connection):
    class Meta:
        node = EmployeeType


class Query(graphene.ObjectType):
    employees = SQLAlchemyConnectionField(EmployeeConnection)
