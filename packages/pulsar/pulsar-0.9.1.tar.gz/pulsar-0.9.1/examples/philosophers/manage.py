'''
The dining philosophers_ problem is an example problem often used in
concurrent algorithm design to illustrate synchronisation issues and
techniques for resolving them.

The problem
===================

Five silent philosophers sit at a round table with each a bowl of spaghetti.
A fork ``f`` is placed between each pair of adjacent philosophers ``P``::


         P     P
         O  f  O
        f       f
     P O         O P
         f     f
            O
            P

Each philosopher ``P`` must alternately think and eat from his bowl ``O``.
Eating is not limited by the amount of spaghetti left: assume an infinite
supply.

However, a philosopher can only eat while holding both the fork ``f`` to
the left and the fork to the right.
Each philosopher can pick up an adjacent fork, when available, and put it down,
when holding it. These are separate actions: forks must be picked up and put
down one by one.

This implementation will just work. No starvation or dead-lock.

There are two parameters:

* Average eating period, the higher the more time is spend eating.
* Average waiting period, the higher the more frequent philosophers
  get a chance to eat.

To run the example, type::

    pulsar manage.py

Implementation
=====================

.. autoclass:: DiningPhilosophers
   :members:
   :member-order: bysource


.. _philosophers: http://en.wikipedia.org/wiki/Dining_philosophers_problem

'''
import os
import random
import json
try:
    import pulsar
except ImportError:
    import sys
    sys.path.append('../../')
    import pulsar
from pulsar import command, task
from pulsar.apps import wsgi, ws, data, ds

# WEB INTERFACE
media_libraries = {
    "d3": "//cdnjs.cloudflare.com/ajax/libs/d3/3.4.2/d3",
    "jquery": "//code.jquery.com/jquery-1.11.0",
    "require": "//cdnjs.cloudflare.com/ajax/libs/require.js/2.1.10/require"
    }
ASSET_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')
FAVICON = os.path.join(ASSET_DIR, 'favicon.ico')


class WsProtocol:

    def encode(self, message):
        return json.dumps(message)

    def decode(self, message):
        return json.loads(message)


###########################################################################
#    EXTRA COMMAND LINE PARAMETERS
class Eating_Period(pulsar.Setting):
    flags = ["--eating-period"]
    validator = pulsar.validate_pos_float
    default = 2
    desc = """The average period of eating for a philosopher."""


class Waiting_Period(pulsar.Setting):
    flags = ["--waiting-period"]
    validator = pulsar.validate_pos_float
    default = 2
    desc = """The average period of waiting for a missing fork."""


###########################################################################
#    PULSAR COMMANDS FOR DINING PHILOSOPHERS
@command(ack=False)
def putdown_fork(request, fork):
    self = request.actor.app
    try:
        self.not_available_forks.remove(fork)
    except KeyError:
        self.logger.error('Putting down a fork which was already available')


@command()
def pickup_fork(request, fork_right):
    self = request.actor.app
    num_philosophers = self.cfg.workers
    fork_left = fork_right - 1
    if fork_left == 0:
        fork_left = num_philosophers
    for fork in (fork_right, fork_left):
        if fork not in self.not_available_forks:
            # Fork is available, send it to the philosopher
            self.not_available_forks.add(fork)
            return fork


############################################################################
#    DINING PHILOSOPHERS APP
class DiningPhilosophers(pulsar.Application):
    description = ('Dining philosophers sit at a table around a bowl of '
                   'spaghetti and waits for available forks.')
    cfg = pulsar.Config(workers=5)

    def monitor_start(self, monitor):
        self.not_available_forks = set()

    def worker_start(self, philosopher, exc=None):
        self._loop = philosopher._loop
        self.eaten = 0
        self.thinking = 0
        self.started_waiting = 0
        self.forks = []
        philosopher._loop.call_soon(self.take_action, philosopher)

    def worker_info(self, philosopher, info=None):
        '''Override :meth:`~.Application.worker_info` to provide
        information about the philosopher.'''
        info['philosopher'] = {'number': philosopher.number,
                               'eaten': self.eaten}

    def take_action(self, philosopher):
        '''The ``philosopher`` performs one of these two actions:

        * eat, if it has both forks and than :meth:`release_forks`.
        * try to :meth:`pickup_fork`, if he has less than 2 forks.
        '''
        loop = philosopher._loop
        forks = self.forks
        if forks:
            #
            # Two forks. Eat!
            if len(forks) == 2:
                self.thinking = 0
                self.eaten += 1
                philosopher.logger.info("eating... So far %s times",
                                        self.eaten)
                eat_time = 2*self.cfg.eating_period*random.random()
                return loop.call_later(eat_time, self.release_forks,
                                       philosopher)
            #
            # One fork only! release fork or try to pick one up one
            elif len(forks) == 1:
                waiting_period = 2*self.cfg.waiting_period*random.random()
                if self.started_waiting == 0:
                    self.started_waiting = loop.time()
                elif loop.time() - self.started_waiting > waiting_period:
                    philosopher.logger.debug("tired of waiting")
                    return self.release_forks(philosopher)
            #
            # this should never happen
            elif len(forks) > 2:    # pragma    nocover
                philosopher.logger.critical('more than 2 forks!!!')
                return self.release_forks(philosopher)
        else:
            if not self.thinking:
                philosopher.logger.warning('%s thinking...', philosopher.name)
            self.thinking += 1
        self.pickup_fork(philosopher)

    @task
    def pickup_fork(self, philosopher):
        '''The philosopher has less than two forks.

        Check if forks are available.
        '''
        fork = yield philosopher.send(philosopher.monitor, 'pickup_fork',
                                      philosopher.number)
        if fork:
            forks = self.forks
            if fork in forks:
                philosopher.logger.error('Got fork %s. I already have it',
                                         fork)
            else:
                philosopher.logger.debug('Got fork %s.', fork)
                forks.append(fork)
        philosopher._loop.call_soon(self.take_action, philosopher)

    def release_forks(self, philosopher):
        '''The ``philosopher`` has just eaten and is ready to release both
        forks.

        This method release them, one by one, by sending the ``put_down``
        action to the monitor.
        '''
        forks = self.forks
        self.forks = []
        self.started_waiting = 0
        for fork in forks:
            philosopher.logger.debug('Putting down fork %s', fork)
            philosopher.send('monitor', 'putdown_fork', fork)
        philosopher._loop.call_later(self.cfg.waiting_period, self.take_action,
                                     philosopher)

    def actorparams(self, monitor, params):
        avail = set(range(1, monitor.cfg.workers+1))
        for philosopher in monitor.managed_actors.values():
            info = philosopher.info
            if info:
                avail.discard(info['philosopher']['number'])
            else:
                avail = None
                break
        number = min(avail) if avail else len(monitor.managed_actors) + 1
        params.update({'name': 'Philosopher %s' % number, 'number': number})


class PhilosophersWsgi(wsgi.LazyWsgi):
    '''This is the :ref:`wsgi application <wsgi-handlers>` for this
    web-chat example.'''
    def __init__(self, server_name):
        self.name = server_name

    def setup(self, environ):
        '''Called once only to setup the WSGI application handler.

        Check :ref:`lazy wsgi handler <wsgi-lazy-handler>`
        section for further information.
        '''
        cfg = environ['pulsar.cfg']
        loop = environ['pulsar.connection']._loop
        self.store = data.create_store(cfg.data_store, loop=loop)
        pubsub = self.store.pubsub(protocol=WsProtocol())
        channel = '%s_messages' % self.name
        pubsub.subscribe(channel)
        middleware = [wsgi.Router('/', get=self.home_page),
                      ws.WebSocket('/message', PhilosopherWs(pubsub, channel)),
                      wsgi.FileRouter('/favicon.ico', FAVICON),
                      wsgi.MediaRouter('media', ASSET_DIR)]
        return wsgi.WsgiHandler(middleware)

    def home_page(self, request):
        doc = wsgi.HtmlDocument(media_path='/media/',
                                known_libraries=media_libraries)
        doc.head.scripts.append('require')
        doc.head.scripts.require('jquery', 'd3', 'philosophers.js')
        doc.head.links.append('bootstrap')
        doc.body.append(wsgi.Html('div', cn='philosophers'))
        return doc.http_response(request)


class PhilosopherWs(ws.WS):

    def __init__(self, pubsub, channel):
        self.pubsub = pubsub
        self.channel = channel

    def on_open(self, websocket):
        '''When a new websocket connection is established it creates a
        new :class:`ChatClient` and adds it to the set of clients of the
        :attr:`pubsub` handler.'''
        self.pubsub.add_client(WsClient(websocket, self.channel))


class WsClient(data.PubSubClient):

    def __init__(self, connection, channel):
        self.connection = connection
        self.channel = channel

    def __call__(self, channel, message):
        self.connection.write(message)


class server(pulsar.MultiApp):
    '''Build a multi-app consisting of

    * The :class:`.DiningPhilosophers` application
    * A wsgi server for displaying actions on the browser
    '''
    cfg = pulsar.Config('Dining philosophers sit at a table around a bowl of '
                        'spaghetti and waits for available forks.',
                        data_store=ds.pulsards_url())

    def build(self):
        yield self.new_app(DiningPhilosophers)
        # yield self.new_app(wsgi.WSGIServer, prefix='wsgi',
        #                    callable=PhilosophersWsgi(self.name))
        # yield self.new_app(wsgi.WSGIServer,
        #                    callable=PhilosophersWsgi(self.name))


if __name__ == '__main__':
    server('philosophers').start()
