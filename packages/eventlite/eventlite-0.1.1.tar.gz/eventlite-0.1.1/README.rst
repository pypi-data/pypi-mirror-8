Eventlite
#########

Light "events" for Python functions.

.. image:: https://pypip.in/version/eventlite/badge.svg?text=version
    :target: https://pypi.python.org/pypi/eventlite/
    :alt: Latest PyPI version

.. image:: https://pypip.in/download/eventlite/badge.svg?period=month
    :target: https://pypi.python.org/pypi/eventlite/
    :alt: Number of PyPI downloads

.. image:: https://pypip.in/py_versions/eventlite/badge.svg
    :target: https://pypi.python.org/pypi/eventlite/
    :alt: Supported Python versions

.. image:: https://pypip.in/status/eventlite/badge.svg
    :target: https://pypi.python.org/pypi/eventlite/
    :alt: Development Status

.. image:: https://pypip.in/license/eventlite/badge.svg
    :target: https://pypi.python.org/pypi/eventlite/
    :alt: License


Abstract
========

The purpose of this library is to provide an "abstract" way for
functions to "report" events, in a way similar to how a logging system
operates.

Some example applications:

- A logging system: ``emit('log', 'My message', level='info')``
- Reporting progress on some running operation ``emit('progress', current=20, total=100)``

Note that the event structure is not imposed in any way; in fact, any
combination of arguments/keywords can be used, proven that the handler
function is able to handle it.


Example usage
=============

.. code-block:: python

    import eventlite

    def myfunction(foo):
        eventlite.emit(foo)

    def handler(foo):
        print('You said: {0}'.format('Hello'))

    with eventlite.handler(handler):
        myfunction('Hello')


API Documentation
=================

The library provides two functions:

- ``eventlite.emit(*a, **kw)`` "emits" an "event" (represented by a
  variable number of arguments / keywords).

- ``eventlite.handler(function)`` returns a context manager that makes
  events to be dispatched to a certain function, while the context is
  active.


So, in the example above, when ``eventlite.emit()`` is called with one
argument, ``handler()`` will be called passing the single argument to
it.


Internals
=========

All the magic is implemented using a ``LocalStack`` (borrowed from
werkzeug) which keeps a stack of handlers to be called, for the local
proxy. The ``emit()`` functon simply looks for an handler in the stack
to which to dispatch the event.

**Note:** by default only the handler for the innermost context
manager is called; this might or might not be the desired behavior;
some way to change this will be added in the future.


Links
=====

- PyPI page: https://pypi.python.org/pypi/eventlite
- Source code: https://github.com/rshk/eventlite
