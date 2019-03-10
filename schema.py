import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField
from schema_department import Department, DepartmentConnections
from schema_employee import Employee, EmployeeConnections


class Query(graphene.ObjectType):
    node = relay.Node.Field()

    employee = relay.Node.Field(Employee)
    employees = SQLAlchemyConnectionField(EmployeeConnections)

    department = relay.Node.Field(Department)
    departments = SQLAlchemyConnectionField(DepartmentConnections)


schema = graphene.Schema(query=Query, types=[Department, Employee])
