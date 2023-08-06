.. -*- coding: utf-8 -*-


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

.. image:: https://dl.dropboxusercontent.com/u/94882440/pydeps.svg

``pydeps`` also contains an Erd__s-like scoring function (a.k.a. Bacon number,
from `Six degrees of Kevin Bacon`_[2]) that lets you filter out modules that
are more than a given number of 'hops' away from the module you're interested in.
This is useful for finding the interface a module has to the rest of the world.


.. _Graphviz: http://www.graphviz.org/Download.php

.. _[2]:: http://en.wikipedia.org/wiki/Six_Degrees_of_Kevin_Bacon


