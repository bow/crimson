# `crimson`

[![pypi](https://img.shields.io/pypi/v/crimson)](https://pypi.org/project/crimson)
[![sourcehut](https://builds.sr.ht/~bow/crimson.svg)](https://builds.sr.ht/~bow/crimson?)


``crimson`` converts non-standard bioinformatics tool outputs to JSON or YAML.

Currently it can convert outputs of the following tools:

  * [FastQC](http://www.bioinformatics.babraham.ac.uk/projects/fastqc/>) (``fastqc``)
  * [FusionCatcher](https://github.com/ndaniel/fusioncatcher) (``fusioncatcher``)
  * [samtools](http://www.htslib.org/doc/samtools.html) flagstat (``flagstat``)
  * [Picard](https://broadinstitute.github.io/picard/) metrics tools (``picard``)
  * [STAR](https://github.com/alexdobin/STAR) log file (``star``)
  * [STAR-Fusion](https://github.com/STAR-Fusion/STAR-Fusion) hits table (``star-fusion``)
  * [Variant Effect Predictor](http://www.ensembl.org/info/docs/tools/vep/index.html)
    plain text output (``vep``)

The conversion can be done using the command line interface or by calling the
tool-specificparser functions in your Python script.


## Installation

``crimson`` is available on the [Python Package Index](https://pypi.org/project/crimson/)
and you can install it via ``pip``:

```shell
$ pip install crimson
```

It is also available on
[BioConda](https://bioconda.github.io/recipes/crimson/README.html), both through the
`conda` package manager or as a
[Docker container](https://quay.io/repository/biocontainers/crimson?tab=tags).


## Usage

### As a command line tool

The general command is `crimson {program_name}` and by default the output is written to
`stdout`. For example, to use the `picard` parser, you would execute:

```shell
$ crimson picard /path/to/a/picard.metrics
```

You can also specify a file name directly to write to a file. The following command will
write the output to a file named ``converted.json``:

```shell
$ crimson picard /path/to/a/picard.metrics converted.json
```

Some parsers may also accept additional input format. The FastQC parser, for example, also
works if you specify a path to a FastQC output directory:


```shell
$ crimson fastqc /path/to/a/fastqc/dir
```

or path to a zipped result:

```shell
$ crimson fastqc /path/to/a/fastqc_result.zip
```

When in doubt, use the ``--help`` flag:

```shell
$ crimson --help            # for the general help
$ crimson fastqc --help     # for parser-specific (FastQC) help
```

### As a Python library function

Generally, the function to import is located at `crimson.{program_name}.parser`. For
example, to use the `picard` parser in your script, you can do:

```python
from crimson import picard

# You can specify the input file name as a string ...
parsed = picard.parse("/path/to/a/picard.metrics")

# ... or a file handle
with open("/path/to/a/picard.metrics") as src:
    parsed = picard.parse(src)
```

## Why?

  * Not enough tools use standard output formats.
  * Writing and re-writing the same parsers across different scripts is not a productive
    way to spend the day.


## Local Development

Setting up a local development requires that you set up all of the supported Python
versions. We recommend using [pyenv](https://github.com/pyenv/pyenv) for this.

The following steps can be your guide for your local development setup:

```shell
# Clone the repository and cd into it.
$ git clone https://git.sr.ht/~bow/crimson
$ cd crimson

# Create your virtualenv.
# If you already have pyenv installed, you may use the Makefile rule below.
$ make dev-pyenv

# Install the package along with its development dependencies.
$ make dev

# Run the test and linter suite to verify the setup.
$ make lint test
```


## Contributing

If you are interested, `crimson` accepts the following types contribution:

  * Documentation additions (if anything seems unclear, feel free to open an issue)
  * Bug reports
  * Support for tools' outputs which can be converted to JSON or YAML.

For any of these, feel free to open an issue in the [issue
tracker](https://github.com/bow/crimson/issues>) or submit a pull request.


## License

``crimson`` is BSD-licensed. Refer to the ``LICENSE`` file for the full license.
