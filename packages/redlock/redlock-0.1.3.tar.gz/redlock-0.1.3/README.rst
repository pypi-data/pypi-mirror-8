.. figure:: https://github.com/glasslion/redlock/raw/master/docs/assets/redlock-small.png
   :alt: RedLock logo

   RedLock logo
RedLock - Distributed locks with Redis and Python
-------------------------------------------------

|Build Status|

This library implements the RedLock algorithm introduced by
[@antirez](http://antirez.com/)

The detailed description of the RedLock algorithm can be found in the
Redis documentation: `Distributed locks with
Redis <http://redis.io/topics/distlock>`__.

The ``redlock.RedLock`` class shares a similar API with the
``threading.Lock`` class in the Python Standard Library.

Simple Usage
~~~~~~~~~~~~

.. code:: python

    from redlock import RedLock
    lock =  RedLock("distributed_lock")
    lock.acquire()
    do_something()
    lock.release()

With Statement / Context Manager
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As with ``threading.Lock``, ``redlock.RedLock`` objects are context
managers thus support the `With
Statement <https://docs.python.org/2/reference/datamodel.html#context-managers>`__.
Thsi way is more pythonic and recommended.

.. code:: python

    from redlock import RedLock
    with RedLock("distributed_lock"):
        do_something()

.. |Build Status| image:: https://travis-ci.org/glasslion/redlock.svg?branch=master
   :target: https://travis-ci.org/glasslion/redlock
