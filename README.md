# graphene-flask-sqlalchemy

## Notes

- The code in https://github.com/graphql-python/graphene-sqlalchemy/tree/master/examples/flask_sqlalchemy differs from the code snippets in https://docs.graphene-python.org/projects/sqlalchemy/en/latest/tutorial/.
  - The former has some extra schema classes that are not necessary.
- I ran into [this issue](https://github.com/graphql-python/graphene-sqlalchemy/issues/153) when running the code copied straight from the SQLAlchemy tutorial. Replacing `DepartmentConnection` with `DepartmentConnections`, as suggested in [this post](https://github.com/graphql-python/graphene-sqlalchemy/issues/153#issuecomment-414441245), fixed the problem.
