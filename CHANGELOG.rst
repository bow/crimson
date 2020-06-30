.. :changelog:

Changelog
=========

This format is based on
`Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_ and this project
adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.


Unreleased
----------


[0.5.2] - 2020-06-30
--------------------

Fixed
~~~~~
* FusionCatcher v1.20 output without any result rows is now parsed properly (see #11).
* Sections in VEP files containing no data is now parsed properly (see #13).


[0.5.1] - 2020-02-27
--------------------

Changed
~~~~~~~
* Relaxed Click and YAML requirements. Now crimon requires only minimum
  versions of these dependencies instead of exact ones.


[0.5.0] - 2020-02-04
--------------------

Added
~~~~~
* Support for parsing output of STAR-Fusion v1.6.0 under the same
  ``star-fusion`` parser. Thank you @Redmar-van-den-Berg!

Removed
~~~~~~~
* Support for Python 2.7, 3.3, 3.4, and 3.5


[0.4.0] - 2018-07-25
--------------------

Added
~~~~~
* Support for parsing zipped FastQC result.

Changed
~~~~~~~
* Improved detection of zipped FastQC input.
* Set configurable file-size limits for flagstat, Picard, and FastQC.


[0.3.0] - 2016-05-19
--------------------

Added
~~~~~
* Support for parsing FusionCatcher final fusion genes file.


[0.2.0] - 2016-04-13
--------------------

Added
~~~~~
* Support for parsing STAR-Fusion hits table output.
* Support for parsing STAR alignment log output.
* Support for parsing VEP plain text output.


[0.1.1] - 2016-02-02
--------------------

Changed
~~~~~~~
* Test and build dependencies.


[0.1.0] - 2015-07-27
--------------------

Added
~~~~~
* First release.
* Support for parsing FastQC, samtools flagstat, and Picard.
