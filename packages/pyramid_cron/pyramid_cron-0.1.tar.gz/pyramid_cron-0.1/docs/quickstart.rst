Quick Start
===========


Install
-------

Install with pip::

    $ pip install pyramid_cron

For each web app which uses pyramid_cron, you'll need to fire the cron handler
from a whitelisted IP once per minute. An easy way to do this is by adding a
cron job on the app server::

    * * * * *   curl -o /dev/null http://localhost/cron


Integrate with a Pyramid App
----------------------------

Include pyramid_cron, by calling ``config.include('pyramid_cron')`` or
adding pyramid_cron to ``pyramid.includes``.


Register a Task
---------------

Register at least one task, using the ``config.add_cron_task()`` directive.
You can also pass a dotted string (e.g. ``myapp.tasks.some_task``) which
will be resolved relative to the calling module.

Tasks are functions which accept a single ``system`` argument. ``system`` is a
dict with two keys: ``request`` and ``registry``, both of which refer to the
Pyramid objects of that name.

.. code-block:: python

    def my_task(system):
        registry = system['registry']
        request = system['request']
        # do stuff

    # Run every 3 hours.
    config.add_cron_task(my_task, hour=(0, 24, 3))

See :doc:`api` for more details.


Request Scope Caveats
---------------------

All tasks that are run during a given minute will be run in the scope of the
same request. This may impose constraints on your tasks, for example:

* Depending on your transaction management infrastructure, tasks will share the
  same SQL session.
* An accumulation of slow tasks may lead to an abnormally long HTTP request,
  tying up resources or exceeding your webserver's timeout threshold.
* Ideally, tasks which are on the slower side should be staggered so that
  they're unlikely to run at the same time.


Logging
-------

Information about task execution (and timing) is logged to the ``pyramid_cron``
handler. If you wish to record it, you should configure logging explicitly for
that handler in your app.
