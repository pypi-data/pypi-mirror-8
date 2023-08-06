'''
A very Simple Web-Socket example.
To run the server type::

    python manage.py

and open a web browser at http://localhost:8060
'''
import os
import sys
from random import random
try:
    import pulsar
except ImportError:  # pragma nocover
    sys.path.append('../../')
    import pulsar

from pulsar.apps import ws, wsgi
from pulsar.utils.pep import range
from pulsar.utils.system import json


DIR = os.path.dirname(__file__)


class Graph(ws.WS):

    def on_open(self, websocket):
        self.on_message(websocket, '')

    def on_message(self, websocket, msg):
        websocket.write(json.dumps([(i, random()) for i in range(100)]))


class Echo(ws.WS):

    def on_message(self, websocket, msg):
        if msg.startswith('send ping '):
            websocket.ping(msg[10:])
        elif msg.startswith('send close '):
            websocket.write_close(int(msg[11:]))
        else:
            websocket.write(msg)


class Site(wsgi.LazyWsgi):

    def setup(self, environ):
        return wsgi.WsgiHandler([wsgi.Router('/', get=self.home),
                                 ws.WebSocket('/data', Graph()),
                                 ws.WebSocket('/echo', Echo())])

    def home(self, request):
        response = request.response
        response.content_type = 'text/html'
        response.encoding = 'utf-8'
        with open(os.path.join(DIR, 'websocket.html')) as f:
            response.content = f.read() % request.environ
        return response


def server(**kwargs):
    return wsgi.WSGIServer(callable=Site(), **kwargs)


if __name__ == '__main__':  # pragma nocover
    server().start()
