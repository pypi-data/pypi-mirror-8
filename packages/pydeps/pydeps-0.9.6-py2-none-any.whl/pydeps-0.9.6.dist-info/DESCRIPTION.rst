pydeps
======

.. image:: https://travis-ci.org/thebjorn/pydeps.svg
   :target: https://travis-ci.org/thebjorn/pydeps


.. image:: https://coveralls.io/repos/thebjorn/pydeps/badge.png
   :target: https://coveralls.io/r/thebjorn/pydeps



Python Dependency visualization. This package installs the ``pydeps``,
and normal usage will be to use it from the command line.

To create graphs you need to install Graphviz_ (make sure the ``dot``
command is on your path).

.. Note:: to display the resulting `.svg` files, it currently calls
          ``firefox foo.svg``.  This is a bug/limitation that will
          hopefully be fixed soon'ish. I would suggest creating a
          script file called ``firefox`` that redirects to your
          favorite viewer if you can't use ``firefox``. Pull requests
          are very welcome.

This is the result of running ``pydeps`` on itself (``pydeps --show pydeps``):


.. _Graphviz: http://www.graphviz.org/Download.php


