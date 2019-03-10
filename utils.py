from graphql_relay.node.node import from_global_id


def global_id_to_db_id(globalId):
    return from_global_id(globalId)[1]
