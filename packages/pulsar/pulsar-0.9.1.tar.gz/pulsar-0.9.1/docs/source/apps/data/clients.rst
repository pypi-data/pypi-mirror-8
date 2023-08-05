.. _data-stores:

=====================
Datastore Clients
=====================

.. automodule:: pulsar.apps.data.store

Getting Started
=====================

To create a data :class:`.Store` client one uses the :func:`.create_store`
function with a valid :ref:`connection string <connection-string>`::

    >>> from pulsar.apps.data import create_store
    >>> store = create_store('redis://user:password@127.0.0.1:6500/11')
    >>> store.name
    'redis'
    >>> store.database
    '11'
    >>> store.dns
    'redis://user:password@127.0.0.1:6500/11'

Additional parameters can be passed via the connection string or as key-valued
parameters. For example::

    >>> store = create_store('redis://user:password@127.0.0.1:6500/11',
                             namespace='test_')
    >>> store.dns
    'redis://user:password@127.0.0.1:6500/11?namespace=test_'


.. _connection-string:

Connection String
~~~~~~~~~~~~~~~~~~~~~~~

The connection string is a way to specify the various parameters for the
data store connection. All :class:`.Store` support a connection string
of the form::

    <scheme>://<username>:<password>@<host>/<database>?param1=...&param2=...


where:

* ``schema`` is the store name
* ``database`` is the database name (or number for redis)
* ``username`` is an optional database username
* ``password`` is an optional database password


Implement a Store
==================

When implementing a new :class:`.Store` there are several methods which need
to be covered:

* :meth:`~Store.ping` to check if the server is available
* :meth:`~Store.connect` to create a new connection
* :meth:`~Store.execute` to execute a command on the store server

These additional methods must be implemented only if the store supports
the :ref:`object data mapper <odm>`:

* :meth:`~Store.execute_transaction` execute a transaction

A new store needs to be registered via the :func:`register_store`
function.

All registered data stores are stored in the ``data_stores`` dictionary::

    from pulsar.apps.data import data_stores

Pulsar provides two implementations, the redis client and the pulsards client.


.. _apps-pubsub:

Publish/Subscribe
=====================

A :class:`.Store` can implement the :meth:`~Store.pubsub` method to return
a valid :class:`.PubSub` handler.


API
============

The main component of the data store API is the :func:`.create_store`
function which creates in one function call a new :class:`.Store`
object which can be used to interact directly with the backend database
or indirectly via the :ref:`object data mapper <odm>`.

Create store
~~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: create_store


Start store
~~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: pulsar.apps.data.stores.pulsards.startds.start_store


Register a new store
~~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: register_store


Store
~~~~~~~~~~~~~~~

.. autoclass:: Store
   :members:
   :member-order: bysource


Command
~~~~~~~~~~~~~~~

.. autoclass:: Command
   :members:
   :member-order: bysource


PubSub
~~~~~~~~~~~~~~~

.. autoclass:: PubSub
   :members:
   :member-order: bysource

