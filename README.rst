Crimson
=======

.. image:: https://travis-ci.org/bow/crimson.svg?branch=master
    :target: https://travis-ci.org/bow/crimson

.. image:: https://coveralls.io/repos/bow/crimson/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/bow/crimson?branch=master


Crimson converts nonstandard bioinformatics tool outputs to a standard format. Currently, the main target output format
is JSON.


Why
---

Because not enough tools use standard output formats.


Setup
-----

Requirements:

    * `virtualenvwrapper <https://virtualenvwrapper.readthedocs.org/en/latest/>`_

.. code-block:: bash

    $ git clone https://github.com/bow/crimson.git
    $ cd crimson
    $ mkvirtualenv -p /usr/bin/python crimson-dev
    $ pip install -r requirements.dev.txt
    $ pip install --editable .


Usage
-----

.. code-block:: bash

    $ crimson --help
