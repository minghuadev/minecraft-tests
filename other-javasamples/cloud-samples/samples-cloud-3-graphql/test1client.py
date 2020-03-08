#!/usr/bin/env python
# test1client.py
#    github.com/prisma-labs/python-graphql-client

from graphqlclient import GraphQLClient
from pprint import PrettyPrinter
import json

server_url = 'http://127.0.0.1:8051/'
#server_url = 'http://swapi.graph.cool/'
client = GraphQLClient(server_url)

# raw dump from playground
query_meta_raw1 = '''{"operationName":"IntrospectionQuery","variables":{},"query":"query IntrospectionQuery {\n  __schema {\n    queryType {\n      name\n    }\n    mutationType {\n      name\n    }\n    subscriptionType {\n      name\n    }\n    types {\n      ...FullType\n    }\n    directives {\n      name\n      description\n      locations\n      args {\n        ...InputValue\n      }\n    }\n  }\n}\n\nfragment FullType on __Type {\n  kind\n  name\n  description\n  fields(includeDeprecated: true) {\n    name\n    description\n    args {\n      ...InputValue\n    }\n    type {\n      ...TypeRef\n    }\n    isDeprecated\n    deprecationReason\n  }\n  inputFields {\n    ...InputValue\n  }\n  interfaces {\n    ...TypeRef\n  }\n  enumValues(includeDeprecated: true) {\n    name\n    description\n    isDeprecated\n    deprecationReason\n  }\n  possibleTypes {\n    ...TypeRef\n  }\n}\n\nfragment InputValue on __InputValue {\n  name\n  description\n  type {\n    ...TypeRef\n  }\n  defaultValue\n}\n\nfragment TypeRef on __Type {\n  kind\n  name\n  ofType {\n    kind\n    name\n    ofType {\n      kind\n      name\n      ofType {\n        kind\n        name\n        ofType {\n          kind\n          name\n          ofType {\n            kind\n            name\n            ofType {\n              kind\n              name\n              ofType {\n                kind\n                name\n              }\n            }\n          }\n        }\n      }\n    }\n  }\n}\n"}'''
query_meta1_m1 = query_meta_raw1.replace('\n', '\\n')

# edited from above raw1
query_meta_raw2 = '''
{
    operationName IntrospectionQuery
    variables{}
    query query IntrospectionQuery {
        __schema {
            queryType {
                name
            }
            mutationType {
                name
            }
            subscriptionType {
                name
            }
            types {
                ...FullType
            }
            directives {
                name
                description
                locations
                args {
                    ...InputValue
                }
            }
        }
    }
    
    fragment FullType on __Type {
        kind
        name
        description
        fields(includeDeprecated: true) {
            name
            description
            args {
                ...InputValue
            }
            type {
                ...TypeRef
            }
            isDeprecated
            deprecationReason
        }
        inputFields {
            ...InputValue
        }
        interfaces {
            ...TypeRef
        }
        enumValues(includeDeprecated: true) {
            name
            description
            isDeprecated
            deprecationReason
        }
        possibleTypes {
            ...TypeRef
        }
    }
    
    fragment InputValue on __InputValue {
        name
        description
        type {
            ...TypeRef
        }
        defaultValue
    }
    
    fragment TypeRef on __Type {
        kind
        name
        ofType {
            kind
            name
            ofType {
                kind
                name
                ofType {
                    kind
                    name
                    ofType {
                        kind
                        name
                        ofType {
                            kind
                            name
                            ofType {
                                kind
                                name
                                ofType {
                                    kind
                                    name
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
'''

# got: Query, String, __Schema, __Type, __TypeKind, Boolean,
#      __Field, __InputValue, __EnumValue, __Directive, __DirectiveLocation
query_meta_raw_ok1 = '''
{
    __schema {
        types {
            name
        }
    }
}
'''

query_meta_raw_ok2 = '''
{
    __schema {
        types { name }, queryType { name }, mutationType { name }, subscriptionType { name }
    }
}
'''

# got:  {'data': {'__type': {'kind': 'OBJECT', 'name': 'Query'}}}
# OBJECT is a value of __TypeKind enum returned by kind
query_meta_raw_ok3 = '''{
    __type(name: "Query"){ name, kind }
}'''

# got:
# fields for an OBJECT
query_meta_raw_ok4 = '''{
    __type(name: "Query"){ name, kind, 
        fields { name, description, type { name, kind } }
    }
}'''

query_sample = '''
{
  hello
}
'''

queries_tested_ok = [
    query_meta_raw_ok1, query_meta_raw_ok2, query_meta_raw_ok3, query_meta_raw_ok4,
    query_sample,
    '',  #json.loads(query_meta1_m1).get("query", None),
    None, #json.loads(query_meta1_m1)
]

for n,q in enumerate(queries_tested_ok):

    print("\nQuery n %d " % n)
    query_meta = q
    tq = type(query_meta)
    if tq is str:
        query = query_meta
        vars = None
        oper = None
        if len(q.strip()) < 2:
            continue
    elif tq is dict:
        query = query_meta.get('query', None)
        vars = query_meta.get('variables', None)
        oper = query_meta.get('operationName', None)
        if query is None or vars is None:
            continue
    else:
        query = ""
        vars = None
        oper = None
        continue
    result = client.execute(query, variables=vars, operationName=oper)

    pp=PrettyPrinter(indent=4)
    pp.pprint(result)

'''result: 
Query n 0 
{   'data': {   '__schema': {   'types': [   {'name': 'Query'},
                                             {'name': 'String'},
                                             {'name': 'Int'},
                                             {'name': '__Schema'},
                                             {'name': '__Type'},
                                             {'name': '__TypeKind'},
                                             {'name': 'Boolean'},
                                             {'name': '__Field'},
                                             {'name': '__InputValue'},
                                             {'name': '__EnumValue'},
                                             {'name': '__Directive'},
                                             {'name': '__DirectiveLocation'}]}}}

Query n 1 
{   'data': {   '__schema': {   'mutationType': None,
                                'queryType': {'name': 'Query'},
                                'subscriptionType': None,
                                'types': [   {'name': 'Query'},
                                             {'name': 'String'},
                                             {'name': 'Int'},
                                             {'name': '__Schema'},
                                             {'name': '__Type'},
                                             {'name': '__TypeKind'},
                                             {'name': 'Boolean'},
                                             {'name': '__Field'},
                                             {'name': '__InputValue'},
                                             {'name': '__EnumValue'},
                                             {'name': '__Directive'},
                                             {'name': '__DirectiveLocation'}]}}}

Query n 2 
{'data': {'__type': {'kind': 'OBJECT', 'name': 'Query'}}}

Query n 3 
{   'data': {   '__type': {   'fields': [   {   'description': None,
                                                'name': 'hello',
                                                'type': {   'kind': 'NON_NULL',
                                                            'name': None}},
                                            {   'description': None,
                                                'name': 'who',
                                                'type': {   'kind': 'SCALAR',
                                                            'name': 'String'}},
                                            {   'description': None,
                                                'name': 'howMany',
                                                'type': {   'kind': 'NON_NULL',
                                                            'name': None}},
                                            {   'description': None,
                                                'name': 'howOld',
                                                'type': {   'kind': 'SCALAR',
                                                            'name': 'Int'}}],
                              'kind': 'OBJECT',
                              'name': 'Query'}}}

Query n 4 
{'data': {'hello': 'Hello, Python-urllib/3.8!...'}}
'''

