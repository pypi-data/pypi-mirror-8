Pyramid Cron
============

Scott Torborg - `Cart Logic <http://www.cartlogic.com>`_

Provides the ability to register simple tasks (callback functions) for
scheduled execution with a cron-like syntax.

Why it's better than a typical task queue like Celery, Resque, etc:

* No user permissions to worry about: everything is run inside a web request,
  so the task has all the same permissions as your web app.
* Very simple setup, no additional daemons required.
* The API follows Pyramid idioms.

Why it's worse:

* It's not well suited to long-running tasks: everything is run inside a web
  request.
* It does not distribute jobs across workers.
* It does not allow for prioritization of jobs, or have any support for
  non-synchronous tasks.


Contents
========

.. toctree::
    :maxdepth: 2

    quickstart
    api
    contributing


Indices and Tables
==================

* :ref:`genindex`
* :ref:`modindex`
