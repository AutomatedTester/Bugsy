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

Getting a bug from Bugzilla
---------------------------
Getting a bug is quite simple. Create a Bugsy object and then get the bug
number that you want.

.. code-block:: python

    import bugsy
    bugzilla = bugsy.Bugsy()
    bug = bugzilla.get(123456)

Creating a new bug
------------------

To create a new bug, create a Bug object, populate it with the items that you need and then
use the Bugsy object to put the bug into Bugzilla

.. code-block:: python

    import bugsy
    bug = bugsy.Bug()
    bug.summary = "I really realy love cheese"
    bug.add_comment("and I really want sausages with it!")

    bugzilla = bugsy.Bugsy("username", "password")
    bugzilla.put(bug)
    bug.id #returns the bug id from Bugzilla

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

.. _Bugsy: