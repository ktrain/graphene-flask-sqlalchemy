from sqlalchemy import *
from sqlalchemy.orm import (scoped_session, sessionmaker, relationship,
                            backref)
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///database.sqlite3', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
# We will need this for querying
Base.query = db_session.query_property()


class Department(Base):
    __tablename__ = 'department'
    id = Column(Integer, primary_key=True)
    name = Column(String)


class Employee(Base):
    __tablename__ = 'employee'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    hired_on = Column(DateTime, default=func.now())
    salary = Column(Integer)
    department_id = Column(Integer, ForeignKey('department.id'))
    department = relationship(
        Department,
        backref=backref('employees',
                        uselist=True,
                        cascade='delete,all'))

    @staticmethod
    def create(data):
        employee = Employee(**data)
        db_session.add(employee)
        db_session.commit()
        return employee

    @staticmethod
    def getPage(page_num, page_size):
        limit = page_size
        offset = (page_num-1) * page_size
        employees = db_session.query(Employee).limit(limit).offset(offset).all()
        return employees

    @staticmethod
    def count():
        return db_session.query(Employee).count()
