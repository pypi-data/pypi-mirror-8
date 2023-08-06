======================
Stack Overflow Watcher
======================
.. image:: https://travis-ci.org/Matt-Deacalion/Stackoverflow-Watcher.svg?branch=master
    :target: https://travis-ci.org/Matt-Deacalion/Stackoverflow-Watcher
    :alt: Build Status
.. image:: https://coveralls.io/repos/Matt-Deacalion/Stackoverflow-Watcher/badge.png?branch=master
    :target: https://coveralls.io/r/Matt-Deacalion/Stackoverflow-Watcher?branch=master
    :alt: Test Coverage
.. image:: https://pypip.in/download/stack-watcher/badge.png?period=week
    :target: https://pypi.python.org/pypi/stack-watcher/
    :alt: Downloads
.. image:: https://pypip.in/version/stack-watcher/badge.png
    :target: https://pypi.python.org/pypi/stack-watcher/
    :alt: Latest Version
.. image:: https://pypip.in/wheel/stack-watcher/badge.png
    :target: https://pypi.python.org/pypi/stack-watcher/
    :alt: Wheel Status
.. image:: https://pypip.in/license/stack-watcher/badge.png
    :target: https://pypi.python.org/pypi/stack-watcher/
    :alt: License

Be the first to answer questions on Stack Exchange web sites with this library
and command line tool to notify you as soon as relevant questions are posted.

Installation
------------

You can install stack-watcher using pip.

.. code-block:: bash

    $ pip install stack-watcher

Basic usage
-----------

Here's how you would watch the latest questions tagged with **`html`**:

.. code-block:: bash

    $ stack-watcher --tag html

Much more can be done, here are some example filters:

+ Questions tagged with *python*
+ Questions tagged with *javascript* and not tagged with *jquery* or *underscore*
+ Questions asked less than an *hour ago* with no answers
+ Questions where the user's *score* is above 100
+ Questions that have been *viewed* over 100 times
+ Questions with the word "*monkey*" in the title

Check out the documentation for more information on customising.

Documentation
-------------

The `latest documentation`_ is hosted by Read the Docs.

Licence
-------
Copyright © 2015 `Matt Deacalion Stevens`_, released under The `MIT License`_.

.. _latest documentation: http://stackoverflow-watcher.readthedocs.org/en/latest/
.. _Matt Deacalion Stevens: http://dirtymonkey.co.uk
.. _MIT License: http://deacalion.mit-license.org
