import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField
import schema_department as Department
import schema_employee as Employee


class Query(Employee.Query, Department.Query, graphene.ObjectType):
    node = relay.Node.Field()


class Mutation(graphene.ObjectType):
    create_employee = Employee.Create.Field()


schema = graphene.Schema(query=Query, mutation=Mutation, types=[
    Department.DepartmentType,
    Employee.EmployeeType
])
