from graphene.test import Client
from schema import schema

def test():
    client = Client(schema)
    executed = client.execute('''
        query employees {
          employees {
            employees {
             id
             name
             hiredOn
             salary
             department {
               id
               name
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
    ''')
    assert executed == {
        'data': {
            'employees': [],
            'pageInfo': {
                'pageNum': 1,
                'pageSize': 3,
                'pageCount': 0,
                'edgeCount': 0
            }
        }
    }

test()
