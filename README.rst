Crimson
=======

|ci| |coverage| |pypi|

.. |ci| image:: https://travis-ci.org/bow/crimson.svg?branch=master
    :target: https://travis-ci.org/bow/crimson

.. |coverage| image:: https://codecov.io/gh/bow/crimson/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/bow/crimson

.. |pypi| image:: https://badge.fury.io/py/Crimson.svg
    :target: http://badge.fury.io/py/crimson

Crimson converts non-standard bioinformatics tool outputs to JSON or YAML.

Currently it accepts outputs of the following programs:

* `FastQC <http://www.bioinformatics.babraham.ac.uk/projects/fastqc/>`_ (``fastqc``)
* `FusionCatcher <https://github.com/ndaniel/fusioncatcher>`_ (``fusioncatcher``)
* `samtools <http://www.htslib.org/doc/samtools.html>`_ flagstat (``flagstat``)
* `Picard <https://broadinstitute.github.io/picard/>`_ metrics tools (``picard``)
* `STAR <https://github.com/alexdobin/STAR>`_ log file (``star``)
* `STAR-Fusion <https://github.com/STAR-Fusion/STAR-Fusion>`_ hits table (``star-fusion``)
* `Variant Effect Predictor <http://www.ensembl.org/info/docs/tools/vep/index.html>`_ plain text output (``vep``)

From those, you can convert the respective output files into JSON (the default) or YAML. You can also use ``crimson``
in your scripts by importing the parser functions themselves.

Installation
------------

Crimson is available via the Python Package Index and you can install it via ``pip``:

.. code-block:: bash

    $ pip install crimson

It is tested on Python 2.7, Python 3.3, and Python 3.4, Python 3.5, and against the following bioinformatics tools:

* FastQC (version 0.10.1)
* FusionCatcher (version 0.99.5a)
* samtools (version 0.19.1, 1.1)
* Picard (version 1.124)
* STAR (version 2.3.0)
* STAR-Fusion (version 0.6.0)
* VEP (version 77)

Usage
-----

Command-line
^^^^^^^^^^^^

The general command is ``crimson {program_name}`` and by default the output is written to ``stdout``. For example,
to use the ``picard`` parser, you would execute:

.. code-block:: bash

    $ crimson picard /path/to/a/picard.metrics

You can also specify a file name directly to write to a file. The following command will write the output to a file
named ``converted.json``:

.. code-block:: bash

    $ crimson picard /path/to/a/picard.metrics converted.json

Some parsers may also accept additional input format. The FastQC parser, for example, also works if you give it a
path to the FastQC output directory:

.. code-block:: bash

    $ crimson fastqc /path/to/a/fastqc/dir

or path to a zipped result:

.. code-block:: bash

    $ crimson fastqc /path/to/a/fastqc_result.zip

When in doubt, use the ``--help`` flag:

.. code-block:: bash

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

    # ... or a file handle directly
    with open("/path/to/a/picard.metrics") as src:
        parsed = picard.parse(src)

Why?
----

* Not enough tools use standard output formats.
* Writing and re-writing the same parsers across different scripts is not a productive way to spend the day.


Contributing
============

If you are interested, Crimson accepts the following types contribution:

* Documentation additions (if anything seems unclear, feel free to open an issue)
* Bug reports
* Support for tools' outputs which can be converted to JSON or YAML.

For any of these, feel free to open an issue in the
`issue tracker <https://github.com/bow/crimson/issues>`_ or submitt a pull request.


License
=======

Crimson is BSD-licensed. Refer to the ``LICENSE`` file for the full license.
