# graphene-flask-sqlalchemy

## Questions
#### What are some of the challenges in implementing this solution on a database that constantly adds, deletes and updates records?
When it is a requirement that the client be able to jump to any page (e.g. the client can numerically specify in the query which page it would like), the total number of records must be exposed to the client. As records are added and deleted, the records shift around on the pages, and as the client moves through the pages, records could be skipped or displayed multiple times.

#### What other approaches can you think of in implementing this solution if some of these constraints does not exist?
Cursor-based pagination is preferable to page number-based pagination when dealing with real-time data because the server enables the client to request pages explicitly based on which records it has seen. Also, since this is the method of pagination that is implemented in Graphene-SQLAlchemy, we get it for free with no additional code required. The downside is that the client cannot jump forward more than a single page at a time, since it must know the cursor to provide to the server.

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

## Implementation

- TIP: When implementing pagination, convert your code away from Relay/SQLAlchemy.
  - The tutorial code makes use of Relay Connections and ConnectionFields to give cursor-based pagination right off the bat.
  - This is convenient, but it is not the style of pagination that is desired. I attempted to extend or override the Relay classes in order to hijack the incoming query parameters and PageInfo in the response, but this proved to be a rabbit hole down which I wasted many hours.
  - Instead, it's much easier to define your own return type rather than try to create a custom Connection.
- TIP: Don't bork your code at 1am.
  - When implementing number-based pagination, I first got the logic under the hood working with hard-coded values in the resolver, since I had trouble setting up the schema to accept values that are different from the `SQLAlchemyConnectionField`. After that, I switched the code away from using Connections entirely and I've implemented pagination and resolvers in a way that looks correct according to my research in the Graphene docs, source code, and Github issue tracker. Unfortunately, the system only ever comes up null, and my resolvers never get called.

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
    pageInfo {
      pageNum
      pageCount
      pageSize
      edgeCount
    }
  }
}

mutation createEmployee {
  createEmployee(input: {
    name: "Testley",
    salary: 2000000,
    departmentId: "RGVwYXJ0bWVudFR5cGU6MQ=="
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
    ok
  }
}

query departments {
  departments {
    edges {
      node {
        id
        name
      }
    }
  }
}
```
