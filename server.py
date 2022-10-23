"""
Module and script providing the multi-progress bar http server.

Adapted from https://gist.github.com/nitaku/10d0662536f37a087e1b
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import cgi
from typing import Type


class ProgressBarServer(BaseHTTPRequestHandler):
    """
    Class defining the HTTP server that hosts the progress bar page(s) and sends and receives data to and from clients.
    """

    def _set_headers(self):
        """
        Set the headers for a non-error response.
        """
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_HEAD(self):
        """
        Handle a request for headers only.
        """
        self._set_headers()

    # GET sends back a Hello world message
    def do_GET(self):
        """
        Handle requests for data from clients.
        """
        self._set_headers()
        self.wfile.write(json.dumps({'hello': 'world', 'received': 'ok'}).encode("utf-8"))

    # POST echoes the message adding a JSON field
    def do_POST(self):
        """
        Handle set sent from clients to update progress bar or accomplish other tasks.
        """
        ctype, _pdict = cgi.parse_header(self.headers.get('content-type'))

        # refuse to receive non-json content
        if ctype != 'application/json':
            self.send_response(400)
            self.end_headers()
            return

        # read the message and convert it into a python dictionary
        length = int(self.headers.get('content-length'))
        message = json.loads(self.rfile.read(length))

        # add a property to the object, just to mess with data
        message['received'] = 'ok'

        # send the message back
        self._set_headers()
        self.wfile.write(json.dumps(message).encode("utf-8"))


def run(server_class: Type[HTTPServer] = HTTPServer,
        handler_class: Type[ProgressBarServer] = ProgressBarServer,
        port: int = 8008):
    """
    Run the progress bar HTTP server.

    Parameters
    ----------
    server_class : Type[HTTPServer]
        Class to use to create server object
    handler_class : Type[ProgressBarServer]
        Class to use to create server handler
    port : int
        Port on which to listen for connections from clients
    """
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)

    print('Starting httpd on port %d...' % port)
    httpd.serve_forever()


if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
