#!/usr/bin/env python
# test1intros.py
#    github.com/prisma-labs/python-graphql-client
#    graphql-core-next.readthedocs.io/en/latest/usage/introspection.html

from graphqlclient import GraphQLClient
from pprint import PrettyPrinter
import json

pp = PrettyPrinter(indent=4)

server_url = 'http://127.0.0.1:8051/'
#server_url = 'http://swapi.graph.cool/'
client = GraphQLClient(server_url)

from graphql import get_introspection_query
#from graphql import graphql_sync
from graphql import build_client_schema
from graphql import print_schema

# query over the network
query_intros = get_introspection_query(descriptions=True)
#introspection_query_result = graphql_sync(schema, query)
intros_result = client.execute(query_intros, variables=None, operationName=None)
client_schema = build_client_schema(intros_result.get('data', None))
sdl = print_schema(client_schema)
print(sdl)
pp.pprint(sdl)
print("\n")

# query again using the graphql_sync()
from graphql import graphql_sync
introspection_query_result = graphql_sync(client_schema, query_intros)
client_schema = build_client_schema(introspection_query_result.data)
sdl = print_schema(client_schema)
print(sdl)
pp.pprint(sdl)
print("\n")

