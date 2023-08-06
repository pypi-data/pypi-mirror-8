ipsync
======

ipsync is a script to update multiple cloud DNS providers with your
external IP address. Useful for when you need to connect to a system on
a dynamic IP.

| |Build Status|
| |Coverage Status|
| |Scrutinizer Code Quality|
| |PyPI Version|

Getting Started
===============

Requirements
------------

-  Python 2.7+ or Python 3.3+

Installation
------------

ipsync can be installed with pip:

::

    $ pip install ipsync

or directly from the source code:

::

    $ git clone https://github.com/jon-walton/ipsync.git
    $ cd ipsync
    $ python setup.py install

Basic Usage
===========

::

    Usage:
        ipsync [options] <command>

    Options:
        -h --help               Show this screen.
        -v --version            Show version.
        -c FILE --config=FILE   Configuration FILE to use [default: ~/.config/ipsync.conf]
        --dry-run               Run but don't make any changes.

    Available commands:
        update                  Resolve current IP address and update all providers

Configuration
-------------

By default, ipsync will look in ~/.config/ipsync.conf for a yaml
formatted file. A sample file is in
`config/config.sample.yml <config/config.sample.yml>`__

**Namecheap.com**

For ipsync to work with namecheap, you must first `enable it within the
control
panel <https://www.namecheap.com/support/knowledgebase/article.aspx/595/11/how-do-i-enable-dynamic-dns-for-a-domain>`__
and then configure a namecheap section within the ipsync configuration
file

::

    namecheap:
      test.com:
        hostname: www
        password: password

      example.com:
        hostname: test
        password: 123456

For Contributors
================

Requirements
------------

-  Make:

   -  Windows: http://cygwin.com/install.html
   -  Mac: https://developer.apple.com/xcode
   -  Linux: http://www.gnu.org/software/make (likely already installed)

-  virtualenv: https://pypi.python.org/pypi/virtualenv#installation
-  Pandoc: http://johnmacfarlane.net/pandoc/installing.html
-  Graphviz: http://www.graphviz.org/Download.php

Installation
------------

Create a virtualenv:

::

    $ mkvirtualenv ipsync
    $ workon ipsync
    $ pip install -r requirements.txt

Run the tests:

::

    $ make test
    $ make tests  # includes integration tests

Run static analysis:

::

    $ make pep8
    $ make pep257
    $ make pylint
    $ make check  # includes all checks

.. |Build Status| image:: http://img.shields.io/travis/jon-walton/ipsync/master.svg
   :target: https://travis-ci.org/jon-walton/ipsync
.. |Coverage Status| image:: http://img.shields.io/coveralls/jon-walton/ipsync/master.svg
   :target: https://coveralls.io/r/jon-walton/ipsync
.. |Scrutinizer Code Quality| image:: http://img.shields.io/scrutinizer/g/jon-walton/ipsync.svg
   :target: https://scrutinizer-ci.com/g/jon-walton/ipsync/?branch=master
.. |PyPI Version| image:: http://img.shields.io/pypi/v/ipsync.svg
   :target: https://pypi.python.org/pypi/ipsync
