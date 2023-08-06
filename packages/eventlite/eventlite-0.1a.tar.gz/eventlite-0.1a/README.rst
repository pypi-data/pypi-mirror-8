Eventlite
#########

Light "events" for Python functions.


Example:

.. code-block:: python

    import eventlite

    def myfunction(foo):
        eventlite.emit(foo)

    def handler(foo):
        print('You said: {0}'.format('Hello'))

    with eventlite.handler(handler):
        myfunction('Hello')
