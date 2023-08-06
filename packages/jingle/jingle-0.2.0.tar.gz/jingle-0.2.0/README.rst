jingle
======

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

.. code:: ini

  one = 1
  two = dos
  three = trzy

Interpolation
^^^^^^^^^^^^^

Basic interpolation is supported thanks to ``SafeConfigParser`` used under the hood:

.. code:: ini

  name = Jon
  surname = Snow
  fullname = %(name)s %(surname)s

Inheritance
^^^^^^^^^^^

Config files can be inherited, or saying precisely included one into another
with ``#inherit`` directive.

In ``defaults.conf``:

.. code:: ini

  host = 0.0.0.0
  port = 3000

In ``production.conf``:

.. code:: ini

  #inherit defaults.conf
  port = 80

Compiled config will use ``host: 0.0.0.0`` and ``port: 80``.

Of course interpolation works across inherited files.

Programatic usage
-----------------

You can as well use the library programatically in your application. Here's 
simple example:

.. code:: python

  from jingle import Template, Context
  
  tpl = Template("Hello {{who}}!")
  print tpl.render(Context("path/to/params.conf"))

License
-------

Copyright (c) 2014 by Kris Kovalik.

Released under MIT license, check LICENSE file for details.
