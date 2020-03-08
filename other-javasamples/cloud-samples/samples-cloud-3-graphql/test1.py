#!/usr/bin/env python

from ariadne import gql, QueryType, make_executable_schema
from ariadne.wsgi import GraphQL

type_defs = gql("""
    type Query {
        hello: String!
        who: String
        howMany: Int!
        howOld: Int
    }
""")

query = QueryType()

@query.field("hello")
def resolve_hello(_, info):
    ##request = info.context["request"]
    ##user_agent = request.headers.get("user-agent", "guest")
    user_agent = info.context["HTTP_USER_AGENT"]
    return "Hello, %s!..." % user_agent #

schema = make_executable_schema(type_defs, query)
application = GraphQL(schema, debug=True)

if __name__ == '__main__':
    do_single = False
    do_loop = True
    from wsgiref.simple_server import make_server
    httpd = make_server('localhost', 8051, application)
    if do_single:
        # Wait for a single request, serve it and quit.
        httpd.handle_request()
    elif do_loop:
        while True:
            httpd.handle_request()
            import time
            time.sleep(0.5)
    else:
        httpd.serve_forever(.5)
    # send a query in playground:
    #    query { hello }
    # or send via curl:
    #    curl 'http://localhost:8051/graphql' \
    #       -H 'Accept-Encoding: gzip, deflate, br' \
    #       -H 'Content-Type: application/json' \
    #       -H 'Accept: application/json' -H 'Connection: keep-alive' \
    #       -H 'DNT: 1' -H 'Origin: http://localhost:8051' \
    #       --data-binary '{"query":"{hello}"}' --compressed

