machete
=======

.. image:: https://pypip.in/version/machete/badge.png
    :target: http://badge.fury.io/py/machete

.. image:: https://travis-ci.org/lovato/machete.png
    :target: https://travis-ci.org/lovato/machete

.. image:: https://pypip.in/py_versions/machete/badge.png

.. image:: https://pypip.in/download/machete/badge.png
        :target: https://crate.io/packages/machete?version=latest

.. image:: https://coveralls.io/repos/lovato/machete/badge.png?branch=develop 
   :target: https://coveralls.io/r/lovato/machete?branch=develop

.. image:: https://pypip.in/format/machete/badge.png

.. image:: https://pypip.in/license/machete/badge.png

A command-line tool to create projects from templates, to start your python work.

To install it
-------------

::

    $ sudo pip install machete

Availability
------------

Production module is available from https://pypi.python.org/pypi/machete/, and development branch is also published by Travis-CI to https://testpypi.python.org/pypi/machete/

Both can be downloaded and installed via the pip command.

Usage
-----

First, create your target directory, and cd to it.

Note: This directory must be empty. If you need to re-run machete, please empty the current folder first.

::

    usage: machete [-h] -t <template_name> [--chicken]

    machete vX

    optional arguments:
      -h, --help            show this help message and exit
      -t <template_name>, --template <template_name>
                            Select one of the available templates. Allowed values
                            are: app, bootstrap or flask.
      --chicken             Chicken mode (optional). Does NOT CHANGE anything.


Contributions
-------------

Bug reports, fixes, or features? Feel free to open an issue or pull request any time.

License
--------

Copyright (c) 2014 Marco Lovato Licensed under MIT_.

.. _MIT: http://opensource.org/licenses/MIT
