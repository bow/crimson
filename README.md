# Crimson

[![pypi](https://img.shields.io/pypi/v/crimson)](https://pypi.org/project/crimson)
[![ci](https://github.com/bow/crimson/actions/workflows/ci.yml/badge.svg)](https://github.com/bow/crimson/actions?query=branch%3Amaster)
[![coverage](https://api.codeclimate.com/v1/badges/7904a5424f60f09ebbd7/test_coverage)](https://codeclimate.com/github/bow/crimson/test_coverage)


Crimson converts non-standard bioinformatics tool outputs to JSON or YAML.

Currently it can convert outputs of the following tools:

  * [FastQC](http://www.bioinformatics.babraham.ac.uk/projects/fastqc/>) (``fastqc``)
  * [FusionCatcher](https://github.com/ndaniel/fusioncatcher) (``fusioncatcher``)
  * [samtools](http://www.htslib.org/doc/samtools.html) flagstat (``flagstat``)
  * [Picard](https://broadinstitute.github.io/picard/) metrics tools (``picard``)
  * [STAR](https://github.com/alexdobin/STAR) log file (``star``)
  * [STAR-Fusion](https://github.com/STAR-Fusion/STAR-Fusion) hits table (``star-fusion``)
  * [Variant Effect Predictor](http://www.ensembl.org/info/docs/tools/vep/index.html)
    plain text output (``vep``)

For each conversion, there are two execution options: as command line tool or as a Python
library function. The first alternative uses `crimson` as a command-line tool. The second one
requires importing the `crimson` library in your program.


## Installation

Crimson is available on the [Python Package Index](https://pypi.org/project/crimson/)
and you can install it via ``pip``:

```shell
$ pip install crimson
```

It is also available on
[BioConda](https://bioconda.github.io/recipes/crimson/README.html), both through the
`conda` package manager or as a
[Docker container](https://quay.io/repository/biocontainers/crimson?tab=tags).

For Docker execution, you may also use
[the GitHub Docker registry](https://github.com/bow/crimson/pkgs/container/crimson). This
registry hosts the latest version, but does not host versions 1.1.0 or earlier.

```shell
docker pull ghcr.io/bow/crimson
```


## Usage

### As a command line tool

The general command is `crimson {tool_name}`. By default, the output is written to
`stdout`. For example, to use the `picard` parser, you would execute:

```shell
$ crimson picard /path/to/a/picard.metrics
```

You can also write the output to a file by specifying a file name. The following
command writes the output to a file named `converted.json`:

```shell
$ crimson picard /path/to/a/picard.metrics converted.json
```

Some parsers may accept additional input formats. The FastQC parser, for example, also
accepts a path to a FastQC output directory as its input:


```shell
$ crimson fastqc /path/to/a/fastqc/dir
```

It also accepts a path to a zipped result:

```shell
$ crimson fastqc /path/to/a/fastqc_result.zip
```

When in doubt, use the ``--help`` flag:

```shell
$ crimson --help            # for the general help
$ crimson fastqc --help     # for the parser-specific help, in this case FastQC
```

### As a Python library function

The specific function to import is generally located at `crimson.{tool_name}.parser`. So to
use the `picard` parser in your program, you can do:

```python
from crimson import picard

# You can specify the input file name as a string or path-like object...
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
versions. We use [pyenv](https://github.com/pyenv/pyenv) for this.

```shell
# Clone the repository and cd into it.
$ git clone https://github.com/bow/crimson
$ cd crimson

# Create your local development environment. This command also installs
# all supported Python versions using `pyenv`.
$ make env

# Run the test and linter suite to verify the setup.
$ make lint test

# When in doubt, just run `make` without any arguments.
$ make
```


## Contributing

If you are interested, Crimson accepts the following types contribution:

  * Documentation updates / tweaks (if anything seems unclear, feel free to open an issue)
  * Bug reports
  * Support for tools' outputs which can be converted to JSON or YAML

For any of these, feel free to open an issue in the [issue
tracker](https://github.com/bow/crimson/issues>) or submit a pull request.


## License

Crimson is BSD-licensed. Refer to the ``LICENSE`` file for the full license.
