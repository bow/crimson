"""Bioinformatics tool outputs converter to JSON or YAML"""

# Copyright (c) 2015-2022 Wibowo Arindrarto <contact@arindrarto.dev>
# SPDX-License-Identifier: BSD-3-Clause

from pathlib import Path
from importlib.metadata import version, PackageNotFoundError


__author__ = "Wibowo Arindrarto"
__contact__ = "contact@arindrarto.dev"
__homepage__ = "https://github.com/bow/crimson"
try:
    __version__ = version(__name__)
except PackageNotFoundError:
    __version__ = "0.0.dev0"

del PackageNotFoundError, Path, version
