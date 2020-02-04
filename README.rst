``crimson``
===========

|pypi| |ci| |cov| |qual|

.. |pypi| image:: https://img.shields.io/pypi/v/crimson?labelColor=4d4d4d&color=007c5b&style=flat
    :target: https://pypi.org/project/crimson/

.. |ci| image:: https://img.shields.io/travis/bow/crimson?labelColor=4d4d4d&color=007c5b&style=flat
    :target: https://travis-ci.org/bow/crimson

.. |cov| image:: https://img.shields.io/codeclimate/coverage/bow/crimson?labelColor=4d4d4d&color=007c5b&style=flat
    :target: https://codeclimate.com/github/bow/crimson

.. |qual| image:: https://img.shields.io/codeclimate/maintainability/bow/crimson?labelColor=4d4d4d&color=007c5b&style=flat
    :target: https://codeclimate.com/github/bow/crimson


``crimson`` converts non-standard bioinformatics tool outputs to JSON or YAML.

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

``crimson`` is available via the Python Package Index and you can install it via ``pip``:

.. code-block:: bash

    $ pip install crimson

It is tested on the following Python versions:

* 3.8
* 3.7
* 3.6

and against the following bioinformatics tools:

* FastQC (version 0.10.1)
* FusionCatcher (version 0.99.5a)
* samtools (version 0.19.1, 1.1)
* Picard (version 1.124)
* STAR (version 2.3.0)
* STAR-Fusion (version 0.6.0, 1.6.0)
* VEP (version 77)

Usage
-----

Command-line
~~~~~~~~~~~~

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
~~~~~~~~~~~~~

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

If you are interested, ``crimson`` accepts the following types contribution:

* Documentation additions (if anything seems unclear, feel free to open an issue)
* Bug reports
* Support for tools' outputs which can be converted to JSON or YAML.

For any of these, feel free to open an issue in the
`issue tracker <https://github.com/bow/crimson/issues>`_ or submitt a pull request.

Local Development
-----------------

Setting up a local development requires any of the supported Python version. It is ideal if you have support Python 2.x
and 3.x versions installed, as that will allow you to run the full tests suite against all versions using ``tox``.

In any case, the following steps can be your guide for setting up your local development environment:

.. code-block:: bash

    # Clone the repository and cd into it
    $ git clone {repo-url}
    $ cd crimson

    # Create your virtualenv, using pyenv for example (recommended, https://github.com/pyenv/pyenv)
    $ pyenv virtualenv 3.7.0 crimson-dev
    # or using virtualenvwrapper (https://virtualenvwrapper.readthedocs.io/en/latest/)
    $ mkvirtualenv -p /usr/bin/python3.7 crimson-dev

    # From within the root directory and with an active virtualenv, install the dependencies and package itself
    $ pip install -e .[dev]


License
=======

``crimson`` is BSD-licensed. Refer to the ``LICENSE`` file for the full license.
