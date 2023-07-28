.. :changelog:

Changelog
=========

This format is based on `Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_ and this
project adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.


Unreleased
----------
*Release date: TBD*

..


1.1.1
-----
*Release date: 28 July 2023*

Changed
^^^^^^^

* Dependencies' versions.

Removed
^^^^^^^

* Explicit Python 3.7 support.

..


1.1.0
-----
*Release date: 11 April 2022*

Added
^^^^^

* Support for parsing STAR-Fusion 1.10 output (thanks @Redmar-van-der-berg).

..


1.0.0
-----
*Release date: 12 October 2021*

Added
^^^^^

* Parsing empty VEP outputs (thanks @Redmar-van-der-berg).
* Support for Python 3.9.

Removed
^^^^^^^

* Support for Python 3.6.

..


1.0.0-alpha1
^^^^^^^^^^^^
*Release date: 2 July 2021*

Added
^^^^^

* `--input-linesep` CLI argument for `picard`, `star`, and `vep` for specifying the line
  separator used when parsing the input file. This is also exposed in the `parser`
  functions as `input_linesep`. For `vep` in particular, this is a backwards-incompatible
  change, as the previous behavior is to always parse using the POSIX new line separator.

..


0.5.2
-----
*Release date: 30 June 2020*

Fixed
^^^^^

* FusionCatcher v1.20 output without any result rows is now parsed properly (see #11).
* Sections in VEP files containing no data is now parsed properly (see #13).

..


0.5.1
-----
*Release date: 27 February 2020*

Changed
^^^^^^^

* Relaxed Click and YAML requirements. Now crimon requires only minimum
  versions of these dependencies instead of exact ones.

..


0.5.0
-----
*Release date: 4 February 2020*

Added
^^^^^

* Support for parsing output of STAR-Fusion v1.6.0 under the same
  ``star-fusion`` parser. Thank you @Redmar-van-den-Berg!

Removed
^^^^^^^

* Support for Python 2.7, 3.3, 3.4, and 3.5

..


0.4.0
-----
*Release date: 25 July 2018*

Added
^^^^^

* Support for parsing zipped FastQC result.

Changed
^^^^^^^

* Improved detection of zipped FastQC input.
* Set configurable file-size limits for flagstat, Picard, and FastQC.

..


0.3.0
-----
*Release date: 19 May 2016*

Added
^^^^^

* Support for parsing FusionCatcher final fusion genes file.

..


0.2.0
-----
*Release date: 13 April 2016*

Added
^^^^^

* Support for parsing STAR-Fusion hits table output.
* Support for parsing STAR alignment log output.
* Support for parsing VEP plain text output.

..


0.1.1
-----
*Release date: 2 February 2016*

Changed
^^^^^^^

* Test and build dependencies.

..


0.1.0
-----
*Release date: 27 July 2015*

Added
^^^^^^^

* First release.
* Support for parsing FastQC, samtools flagstat, and Picard.
