.. Bugzilla documentation master file, created by
   sphinx-quickstart on Sat May 31 20:43:30 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Bugsy!
=================

Bugsy is a tool that allows you to programmatically work with Bugzilla using its native REST API.

To use you will do

.. code-block:: python

    import bugsy
    bugzilla = bugsy.Bugsy()
    bug = bugzilla.get(123456)
    bug123456.status = 'RESOLVED'
    bug123456.resolution = 'FIXED'
    bugzilla.put(bug123456)


To see further details look at:

.. toctree::
   :maxdepth: 2

   bugsy.rst
   bug.rst


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

