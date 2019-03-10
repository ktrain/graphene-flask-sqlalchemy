import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models import db_session, Employee as EmployeeModel
import utils


class EmployeeBase:
    name = graphene.String(description="Name of the Employee", required=True)
    salary = graphene.Int(description="Employee's salary")
    hired_on = graphene.types.datetime.DateTime(description="Timestamp of the Employee's hiring")
    department_id = graphene.String(description="ID of the Employee's Department")


class EmployeeType(SQLAlchemyObjectType, EmployeeBase):
    class Meta:
        model = EmployeeModel
        interfaces = (relay.Node, )


class EmployeeConnection(relay.Connection):
    class Meta:
        node = EmployeeType


class Query(graphene.ObjectType):
    employees = SQLAlchemyConnectionField(EmployeeConnection)


class EmployeeInput(EmployeeBase, graphene.InputObjectType):
    pass


class CreateEmployee(graphene.Mutation):
    class Arguments:
        input = EmployeeInput(required=True)

    employee = graphene.Field(EmployeeType)
    ok = graphene.Boolean()

    def mutate(self, info, input):
        ok = False
        if ('department_id' in input):
            input['department_id'] = utils.global_id_to_db_id(input['department_id'])
        employee = EmployeeModel(**input)
        db_session.add(employee)
        db_session.commit()
        ok = True

        return CreateEmployee(employee=employee, ok=ok)


class Mutation(graphene.ObjectType):
    create_employee = CreateEmployee.Field(description="Create a new Employee")


