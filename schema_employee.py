import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models import db_session, Employee as EmployeeModel


class Employee(SQLAlchemyObjectType, EmployeeAttribute):
    class Meta:
        model = EmployeeModel
        interfaces = (relay.Node, )


class EmployeeConnections(relay.Connection):
    class Meta:
        node = Employee
