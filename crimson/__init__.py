# -*- coding: utf-8 -*-
"""
    crimson
    ~~~~~~~

    :license: BSD

    Converter for various bioinformatics tool outputs.

"""
# (c) 2015-2020 Wibowo Arindrarto <bow@bow.web.id>

from pathlib import Path

from single_source import get_version


__author__ = "Wibowo Arindrarto"
__contact__ = "bow@bow.web.id"
__homepage__ = "http://bow.web.id"
__version__ = get_version(__name__, Path(__file__).parent.parent)

del Path, get_version
