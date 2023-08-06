TCP to Canopsis connector
=========================

.. image:: https://travis-ci.org/linkdd/tcp2canopsis.svg?branch=master


This package provides a connector which listen for events on a TCP port.

Usage
-----

Run the script on a designated port (``8000`` in this example) and with the URL
of the AMQP server :

.. code-block::

   $ tcp2canopsis -p 8000 -a "amqp://guest:guest@localhost:5672/"

Then use ``telnet`` to publish events :

.. code-block::

   $ telnet localhost 8000
   Trying ::1...
   Connected to localhost.
   Escape character is '^]'.
   {"connector": "test", "connector_name": "testname", "event_type": "check", "source_type": "resource", "component": "testcmp", "resource": "testrsrc", "state": 0, "output": "test output"}
   {"connector": "test", "connector_name": "testname", "event_type": "check", "source_type": "resource", "component": "testcmp", "resource": "testrsrc", "state": 1, "output": "test output 2"}
   {"connector": "test", "connector_name": "testname", "event_type": "check", "source_type": "resource", "component": "testcmp", "resource": "testrsrc", "state": 0, "output": "test output 3"}
   Connection closed by foreign host.

Or in a JSON file :

.. code-block:: javascript

   {"tcp2canopsis": {
       "port": 8000,
       "amqp": "amqp://guest:guest@localhost:5672/"
   }}

And load the file using :

.. code-block::

   $ tcp2canopsis -c path/to/config.json

Installation
------------

Just type :

.. code-block::

   $ pip install tcp2canopsis

Or, to install it in a locally :

.. code-block::

   $ ./makefile

This will create a virtual Python environment in the current folder, and install the dependencies listed by ``requirements.txt``.
Finally, it will perform a ``python setup.py install``.

After executing this script, the connector will be available in the current folder (which is now a virtual Python environment).
