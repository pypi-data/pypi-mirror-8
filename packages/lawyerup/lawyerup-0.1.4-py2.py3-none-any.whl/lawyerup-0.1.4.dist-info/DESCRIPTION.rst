=============================
LawyerUp
=============================

.. image:: https://travis-ci.org/redjack/lawyerup.png?branch=master
    :target: https://travis-ci.org/redjack/lawyerup

LawyerUp adds license headers to your code.

Inspired by lice_.

.. _lice: https://github.com/licenses/lice

Installation
------------

::

  pip install lawyerup


Usage
-----

::

  $ lawyerup --help
  usage: lawyerup [-h] [--vars | --context [KEY=VALUE [KEY=VALUE ...]]] LICENSE

  Add license headers to files passed in on stdin

  positional arguments:
    LICENSE               the license to add, one of GPR, GRR, generic

  optional arguments:
    -h, --help            show this help message and exit
    --vars                list template variables for specified license
    --context [KEY=VALUE [KEY=VALUE ...]]
                          KEY=VALUE formatted variables to generate the license


::

  $ cat list-of-files | lawyerup <license> --context KEY1=VAL1 KEY2=VAL2 ...


Available Licenses
------------------

* Government Purpose Rights (``GPR``)
* Government Restricted Rights (``GRR``)
* Generic "see COPYING file in the root of this distribution" (``generic``)






History
-------

0.1.4 (2014-11-20)
++++++++++++++++++

* Bugfix: Python 2.6 requires ``argparse``.
* Stylus support.

0.1.3 (2013-12-16)
++++++++++++++++++

* Bugfix: Strip trailing whitespace from formatted headers.

0.1.2 (2013-11-13)
++++++++++++++++++

* Bugfix: Don't die on empty files.
* Bugfix: Treat all input files as UTF-8.

0.1.1 (2013-11-13)
++++++++++++++++++

* Bugfix release. Actually include the license headers in the distribution.

0.1.0 (2013-11-13)
++++++++++++++++++

* First release. Add headers to lists of files read from ``stdin``.


