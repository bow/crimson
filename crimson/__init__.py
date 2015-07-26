# -*- coding: utf-8 -*-
# flake8: noqa
"""
    crimson
    ~~~~~~~

    :copyright: (c) 2015 Wibowo Arindrarto <bow@bow.web.id>
    :license: BSD

"""

RELEASE = False

__version_info__ = ("0", "1", "0")
__version__ = ".".join(__version_info__)
__version__ += "-dev" if not RELEASE else ""

__author__ = "Wibowo Arindrarto"
__contact__ = "bow@bow.web.id"
__homepage__ = "http://bow.web.id"


from .fastqc import parse_fastqc
from .flagstat import parse_flagstat
from .picard import parse_picard
