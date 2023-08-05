Master Password
===============

This is a Python implementation of the `Master Password algorithm`__ by
`Maarten Billemont`__. It also comes with a command line interface that lets
you compute passwords for your sites based on your master password.

__ http://masterpasswordapp.com/algorithm.html
__ http://lhunath.com


Installation
------------

This package requires Python 3 (tested with 3.4) and uses `scrypt`__ (you need
a compiler for this) and
`click`__.

Installation with `pip`__:

.. code-block:: bash

   $ pip install mpw

This app copies the password to the clipboard. This should work out-of-the-box
on OS X and Windows. On Linux, *mpw* makes use of the ``xclip`` or ``xsel`` commands, which should come with the os. Otherwise run:

.. code-block:: bash

   $ sudo apt-get install xclip
   $ # or
   $ sudo apt-get install xsel

Alternatively, the gtk or PyQT4 modules can be installed.

Binary executables (e.g., an installer for Windows) may follow.

__ https://pypi.python.org/pypi/scrypt
__ https://pypi.python.org/pypi/click
__ https://pypi.python.org/pypi/pip


Usage
-----

.. code-block:: bash

   $ mpw get pypi
   Enter your name: Alice
   Enter master password: s3cr3d!
   Password for pypi for user Alice was copied to the clipboard.


For more information take a look at the help:

.. code-block:: bash

   $ mpw --help
