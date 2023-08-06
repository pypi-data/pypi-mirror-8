jingle
======

**Config files renderer based on Jinja2.**

It renders template files with context loaded from simple INI-style config files.
Config files support inheritance_ and interpolation_.

Getting started
---------------

Install this package with *pip*:
::

  $ pip install jingle
  
Check usage:
::

  $ jingle --help
   
Run some examples:
::

  $ jingle examples/hello.conf < examples/hello.j2
   
Config files
------------

*Jingle* supports single-group INI config files. For example:

.. code:: yaml

  one: 1
  two: dos
  three: trzy

Interpolation
^^^^^^^^^^^^^

Basic interpolation is supported thanks to ``SafeConfigParser`` used under the hood:

.. code:: yaml

  name: Jon
  surname: Snow
  fullname: %(name)s %(surname)s

Inheritance
^^^^^^^^^^^

Config files can be inherited, or saying precisely included one into another
with ``#inherit`` directive.

In ``defaults.conf``:

.. code:: yaml

  host: 0.0.0.0
  port: 3000

In ``production.conf``:

.. code:: yaml

  #inherit defaults.conf
  port: 80

Compiled config will use ``host: 0.0.0.0`` and ``port: 80``.

Of course interpolation works across inherited files.

Hacking
-------

If you plan to contribute to the project or just wanna play around, it's dead simple.

1. Install dependencies with *pip*:

   ::

     $ pip install distutils jinja2
  
2. Hack your way through.

3. Feel free to add new ones to ``test.sh``, then check if they're passing:

   ::

     $ ./test.sh
  
4. Install locally to make sure everything works:

   ::

     $ python setup.py install
  
Enjoy!
  
License
-------

Copyright (c) 2014 by Kris Kovalik.

Released under MIT license, check `license file`_ file for details.

.. _`license file`: LICENSE
