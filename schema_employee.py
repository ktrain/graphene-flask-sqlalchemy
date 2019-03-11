import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models import db_session, Employee as EmployeeModel
import utils
import math


class PaginationInfo(graphene.ObjectType):
    page_num = graphene.Int(description="Current page number")
    page_count = graphene.Int(description="Total number of pages")
    page_size = graphene.Int(description="Number of edges per page")
    edge_count = graphene.Int(description="Total number of edges")


class EmployeeBase:
    name = graphene.String(description="Name of the Employee", required=True)
    salary = graphene.Int(description="Employee's salary")
    hired_on = graphene.types.datetime.DateTime(description="Timestamp of the Employee's hiring")
    department_id = graphene.String(description="ID of the Employee's Department")


class EmployeeType(SQLAlchemyObjectType, EmployeeBase):
    class Meta:
        model = EmployeeModel
        interfaces = (relay.Node, )


class EmployeePage(graphene.ObjectType):
    employees = graphene.List(EmployeeType)
    page_info = graphene.Field(PaginationInfo)

    def resolve_employees(self, info, **args):
        print 'resolving employees'
        page_num = args.get('page_num') or 1
        page_size = args.get('page_size') or 3

        employees = EmployeeModel.getPage(page_num, page_size)
        return [ EmployeeType(employee) for employee in employees ]

    def resolve_page_info(self, info, **args):
        print 'resolving page info'
        page_num = args.get('page_num') or 1
        page_size = args.get('page_size') or 3
        edge_count = EmployeeModel.count()
        page_count = math.ceil(float(edge_count)/page_size)

        return PaginationInfo(
            page_num=page_num,
            page_count=page_count,
            page_size=page_size,
            edge_count=edge_count
        )


class Query(graphene.ObjectType):
    employee = relay.Node.Field(EmployeeType)
    employees = graphene.Field(
        EmployeePage,
        description="Get a page of Employees",
        page_num=graphene.Int(),
        page_size=graphene.Int()
    )


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
        employee = EmployeeModel.create(input)
        ok = True

        return CreateEmployee(employee=employee, ok=ok)


class Mutation(graphene.ObjectType):
    create_employee = CreateEmployee.Field(description="Create a new Employee")


