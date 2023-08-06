|Build Status|

[Py]thon [M]ultiple-[R]epository Managment Tool
===============================================

Installation
============

``pip install pymr``

or

::

    git clone https://github.com/kpurdon/pymr.git
    cd pymr
    python setup.py install

Running
=======

Available Commands
------------------

To view help enter:

::

    pymr-register --help
    pymr-run --help

Register Directories
--------------------

In any directory you want to run a command on enter the following
command (pymr-register)

You can optionally add tags to the register command. This will allow you
to run commands on only those directories with a set of tags
(pymr-register -t foo)

Run Commands
------------

In any directory you can run the command: ``pymr-run [cmd]``

This command will recurse finding all .pymr files created by
pymr-register.

Example
=======

Given the following directory structure:

::

    ├── foo
    │   ├── bar
    │   ├── baz
    │   └── foo

Lets register the bar & baz directories with the tag "test":

::

    cd foo/bar && pymr-register -t test
    cd foo/baz && pymr-register -t test

Lets register the foo directory with the tag "default":

::

    cd foo/foo && pymr-register

Now, say we want to run "ls -la" for the bar/baz directories. From ANY
directory above them run:

::

    pymr-run -t test "ls -la"

.. |Build Status| image:: https://travis-ci.org/kpurdon/pymr.svg?branch=master
   :target: https://travis-ci.org/kpurdon/pymr


