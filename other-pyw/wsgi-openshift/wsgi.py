#!/usr/bin/python
import os

virtenv = os.environ['OPENSHIFT_PYTHON_DIR'] + '/virtenv/'
virtualenv = os.path.join(virtenv, 'bin/activate_this.py')
try:
    execfile(virtualenv, dict(__file__=virtualenv))
except IOError:
    pass
#
# IMPORTANT: Put any additional includes below this line.  If placed above this
# line, it's possible required libraries won't be in your searchable path
#

def application(environ, start_response):

    ctype = 'text/plain'
    if environ['PATH_INFO'] == '/health':
        response_body = "1"
    elif environ['PATH_INFO'] == '/env':
        response_body = ['%s: %s' % (key, value)
                    for key, value in sorted(environ.items())]
        response_body = '\n'.join(response_body)
    elif environ['PATH_INFO'] == '/pysrc':
        import sys
        #sys.path.append('./pysrc')
        #see http://stackoverflow.com/questions/8943421/cannot-import-module
        EXTDIR = os.path.realpath(os.path.join(os.path.dirname(__file__), 'pysrc'))
        if EXTDIR not in sys.path:
            sys.path.append(EXTDIR)
        import wsgisub
        response_list = wsgisub.application(environ, start_response)
        ctype = response_list[0]
        response_body = response_list[1]
    else:
        ctype = 'text/html'
        response_body = '''
<html lang="en"> <head> <title>Welcome to OpenShift</title> </head>
<body>
            <h1>Welcome to your Python application on OpenShift</h1>
                <h2>Managing your application</h2>
                <h3>Web Console</h3>
                <h3>Command Line Tools</h3>
</body>
</html>'''

    status = '200 OK'
    response_headers = [('Content-Type', ctype), ('Content-Length', str(len(response_body)))]
    #
    start_response(status, response_headers)
    return [response_body]

#
# Below for testing only
#
if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    httpd = make_server('localhost', 8051, application)
    # Wait for a single request, serve it and quit.
    httpd.handle_request()
