#!/usr/bin/env python
#   sample1.py

from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import datetime
import os

port = 8000

class myHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/time':
            self.do_time()
        elif self.path.startswith('/upload/'):
            self.do_command()
        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            # Send the html message
            self.wfile.write("<b> Hello World !</b>")
            #self.wfile.close()

    def do_time(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        # Send the html message
        self.wfile.write("<b> Hello World !</b>"
                         + "<br><br>Current time: " + str(datetime.datetime.now()))

    def do_command(self):
        path_segs = self.path.split('/')
        if type(path_segs) is list and len(path_segs) >= 3 and path_segs[1] == 'upload':
            seqn = int(path_segs[2])
            if os.path.isdir("upload/%d" % seqn):
                self.send_response(200) # ok
            else:
                self.send_response(404) # not found
        else:
            self.send_response(400)  # bad request

    def do_POST(self):
        if self.path.startswith('/upload/'):
            length = self.headers['content-length']
            data = self.rfile.read(int(length))
            dlen = len(data)

            path_segs = self.path.split('/')
            if dlen != length:
                self.send_response(406)  # not acceptable
            elif type(path_segs) is list and len(path_segs) >= 4 and path_segs[1] == 'upload':
                seqn = int(path_segs[2])
                fn = path_segs[3]
                fpth = "upload/%s/%s" % (seqn, fn)

                print("received dlen %d" % dlen)

                if not os.path.isdir("upload"):
                    os.mkdir("upload")
                if not os.path.isdir("upload/%d" % seqn):
                    os.mkdir("upload/%d" % seqn)

                with open(fpth, 'wb') as fh:
                    fh.write(data)

                self.send_response(200) # ok
            else:
                self.send_response(404) # not found
        else:
            self.send_response(400)  # bad request

server = HTTPServer(('', port), myHandler)
print 'Started httpserver on port ', port

#Wait forever for incoming http requests
server.serve_forever()

