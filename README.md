# graphene-flask-sqlalchemy

## Notes

- Make sure you use Python 2.
  - For Mac users, `brew install python@2` is all you need to do to prep.
- The code in the [Graphene SQLAlchemy + Flask tutorial](https://github.com/graphql-python/graphene-sqlalchemy/tree/master/examples/flask_sqlalchemy) differs from the code snippets in the [referenced Git repo](https://docs.graphene-python.org/projects/sqlalchemy/en/latest/tutorial/).
  - I recommend ignoring the repo and sticking to the tutorial.
  - The former has some extra schema classes that are not necessary.
  - The difference in code made it difficult to apply the fix in the next bullet.
  - Using the `requirements.txt` in the repo gives you outdated package versions.
- I ran into [this issue](https://github.com/graphql-python/graphene-sqlalchemy/issues/153) when running the code copied straight from the SQLAlchemy tutorial.
  - Replacing `DepartmentConnection` with `DepartmentConnections`, as suggested in [this post](https://github.com/graphql-python/graphene-sqlalchemy/issues/153#issuecomment-414441245), fixed the problem.
  - For consistency, I did the same for `EmployeeConnection`.

## Resources

- https://www.howtographql.com/graphql-python/0-introduction/
- https://github.com/alexisrolland/flask-graphene-sqlalchemy/wiki/Flask-Graphene-SQLAlchemy-Tutorial


## Queries

```graphql
query employees {
  employees {
    edges {
      node {
        id
        name
        hiredOn
        salary
        department {
          id
          name
        }
      }
    }
  }
}

mutation createEmployee {
  createEmployee(input: {
    name: "Testley",
    salary: 2000000,
    departmentId: ""
  }) {
    employee {
      id
      name
      hiredOn
      salary
      department {
        id
        name
      }
    }
  }
}

```
