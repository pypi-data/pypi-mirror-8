Hacking
=======

If you plan to contribute to the project or just wanna play around, follow the steps:

1. Install *virtualenv*, then create your dev env with our custom command:

   ::

     $ pip install virtualenv
     $ ./hacking/prepare

2. Hop into dev environment:

   ::

     $ source hacking/env/bin/activate

3. Install development requirements:

   ::

     $ ./hacking/requirements

4. Hack your way through.

5. Add tests for stuff you've changed. Don't forget to run tests:

   ::

     $ ./hacking/test

7. To deactivate virtualenv, simply run:

   ::

     $ deactivate

Enjoy!

Manual testing
--------------

If you want to run some stuff manually, you need to perform installation of the package
first. Whenever you made some changes and wanna manually check them out (eg. by executing
the ``jingle`` binary from console), do this:

::

  $ hacking/testinstall

IMPORTANT! Remember to run this command with active virtualenv.
