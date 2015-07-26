Crimson
=======

.. image:: https://travis-ci.org/bow/crimson.svg?branch=master
    :target: https://travis-ci.org/bow/crimson

.. image:: https://coveralls.io/repos/bow/crimson/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/bow/crimson?branch=master


Crimson converts nonstandard bioinformatics tool outputs to a standard format. Currently it accepts outputs of the
following programs:

* `FastQC <http://www.bioinformatics.babraham.ac.uk/projects/fastqc/>`_ (``fastqc``)
* `samtools <http://www.htslib.org/doc/samtools.html>`_ flagstat (``flagstat``)
* `Picard <https://broadinstitute.github.io/picard/>`_ metrics tools (``picard``)

From those, you can convert the respective output files into JSON (the default) or YAML. You can also use ``crimson``
in your scripts by importing the parser functions themselves.


Usage
-----

Command-line
^^^^^^^^^^^^

The general command is ``crimson {program_name}`` and by default the output is written to ``stdout``, for example:

.. parsed-literal::

    $ crimson picard /path/to/a/picard.metrics

You can also specify a file name directly to write to a file. The following command will write the output to a file
named ``converted.json``:

.. parsed-literal::

    $ crimson picard /path/to/a/picard.metrics converted.json

Some parsers may also accept additional input format. The FastQC parser, for example, also works if you give it a
path to the FastQC output directory:

.. parsed-literal::

    $ crimson fastqc /path/to/a/fastqc/dir

When in doubt, use the ``--help`` flag:

.. parsed-literal::

    $ crimson --help            # for the general help
    $ crimson fastqc --help     # for parser-specific (FastQC) help

Python Module
^^^^^^^^^^^^^

The function to import is located at ``crimson.{program_name}.parser``. So to use the ``picard`` parser in your script,
you can do this:

.. code-block:: python

    from crimson import picard

    # You can supply the file name as string ...
    parsed = picard.parse("/path/to/a/picard.metrics")

    # ... or s a file handle directly
    with open("/path/to/a/picard.metrics") as src:
        parsed = picard.parse(src)

Crimson is tested against Python 2.7, Python 3.3, and Python 3.4.

Why
---

* Not enough tools use standard output formats.
* I got tired of writing and re-writing the same parsers across different scripts.
