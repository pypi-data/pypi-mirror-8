'''Tests the websocket middleware in pulsar.apps.ws.'''
import unittest

from pulsar import asyncio, send, new_event_loop
from pulsar.apps.ws import WebSocket, WS
from pulsar.apps.http import HttpClient
from pulsar.apps.test import dont_run_with_thread

from .manage import server


class Echo(WS):

    def __init__(self, loop):
        self.queue = asyncio.Queue(loop=loop)

    def get(self):
        return self.queue.get()

    def on_message(self, ws, message):
        self.queue.put_nowait(message)

    def on_ping(self, ws, body):
        ws.pong(body)
        self.queue.put_nowait('PING: %s' % body.decode('utf-8'))

    def on_pong(self, ws, body):
        self.queue.put_nowait('PONG: %s' % body.decode('utf-8'))

    def on_close(self, ws):
        self.queue.put_nowait('CLOSE')


class TestWebSocketThread(unittest.TestCase):
    app_cfg = None
    concurrency = 'thread'

    @classmethod
    def setUpClass(cls):
        s = server(bind='127.0.0.1:0', name=cls.__name__,
                   concurrency=cls.concurrency)
        cls.app_cfg = yield send('arbiter', 'run', s)
        addr = cls.app_cfg.addresses[0]
        cls.uri = 'http://{0}:{1}'.format(*addr)
        cls.ws_uri = 'ws://{0}:{1}/data'.format(*addr)
        cls.ws_echo = 'ws://{0}:{1}/echo'.format(*addr)

    @classmethod
    def tearDownClass(cls):
        if cls.app_cfg is not None:
            yield send('arbiter', 'kill_actor', cls.app_cfg.name)

    def testHyBiKey(self):
        w = WebSocket('/', None)
        v = w.challenge_response('dGhlIHNhbXBsZSBub25jZQ==')
        self.assertEqual(v, "s3pPLMBiTxaQ9kYGzzhZRbK+xOo=")

    def testBadRequests(self):
        c = HttpClient()
        response = yield c.post(self.ws_uri)
        self.assertEqual(response.status_code, 405)
        #
        response = yield c.get(self.ws_uri,
                               headers=[('Sec-Websocket-Key', 'x')])
        self.assertEqual(response.status_code, 400)
        #
        response = yield c.get(self.ws_uri,
                               headers=[('Sec-Websocket-Key', 'bla')])
        self.assertEqual(response.status_code, 400)
        #
        response = yield c.get(self.ws_uri,
                               headers=[('Sec-Websocket-version', 'xxx')])
        self.assertEqual(response.status_code, 400)

    def test_upgrade(self):
        c = HttpClient()
        handler = Echo(c._loop)
        ws = yield c.get(self.ws_echo, websocket_handler=handler)
        response = ws.handshake
        self.assertEqual(response.status_code, 101)
        self.assertEqual(response.headers['upgrade'], 'websocket')
        self.assertEqual(ws.connection, response.connection)
        self.assertEqual(ws.handler, handler)
        #
        # on_finished
        self.assertTrue(response.on_finished.done())
        self.assertFalse(ws.on_finished.done())
        # Send a message to the websocket
        ws.write('Hi there!')
        message = yield handler.get()
        self.assertEqual(message, 'Hi there!')

    def test_ping(self):
        c = HttpClient()
        handler = Echo(c._loop)
        ws = yield c.get(self.ws_echo, websocket_handler=handler)
        #
        # ASK THE SERVER TO SEND A PING FRAME
        ws.write('send ping TESTING PING')
        message = yield handler.get()
        self.assertEqual(message, 'PING: TESTING PING')

    def test_pong(self):
        c = HttpClient()
        handler = Echo(c._loop)
        ws = yield c.get(self.ws_echo, websocket_handler=handler)
        #
        ws.ping('TESTING CLIENT PING')
        message = yield handler.get()
        self.assertEqual(message, 'PONG: TESTING CLIENT PING')

    def test_close(self):
        c = HttpClient()
        handler = Echo(c._loop)
        ws = yield c.get(self.ws_echo, websocket_handler=handler)
        self.assertEqual(ws.event('post_request').fired(), 0)
        ws.write('send close 1001')
        message = yield handler.get()
        self.assertEqual(message, 'CLOSE')
        self.assertTrue(ws.close_reason)
        self.assertEqual(ws.close_reason[0], 1001)
        self.assertTrue(ws._connection.closed)

    def test_close_sync(self):
        loop = new_event_loop()
        c = HttpClient(loop=loop)
        handler = Echo(loop)
        ws = c.get(self.ws_echo, websocket_handler=handler)
        self.assertEqual(ws.event('post_request').fired(), 0)
        self.assertEqual(ws._loop, loop)
        self.assertFalse(ws._loop.is_running())
        ws.write('send close 1001')
        message = ws._loop.run_until_complete(handler.get())
        self.assertEqual(message, 'CLOSE')
        self.assertTrue(ws.close_reason)
        self.assertEqual(ws.close_reason[0], 1001)
        self.assertTrue(ws._connection.closed)

    def test_home(self):
        c = HttpClient()
        response = yield c.get(self.uri)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['content-type'],
                         'text/html; charset=utf-8')

    def test_graph(self):
        c = HttpClient()
        handler = Echo(c._loop)
        ws = yield c.get(self.ws_uri, websocket_handler=handler)
        self.assertEqual(ws.event('post_request').fired(), 0)
        message = yield handler.get()
        self.assertTrue(message)


@dont_run_with_thread
class TestWebSocketProcess(TestWebSocketThread):
    concurrency = 'process'
