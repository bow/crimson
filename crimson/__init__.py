"""Bioinformatics tool outputs converter to JSON or YAML"""
# (c) 2015-2021 Wibowo Arindrarto <contact@arindrarto.dev>

from pathlib import Path

from single_source import get_version


__author__ = "Wibowo Arindrarto"
__contact__ = "contact@arindrarto.dev"
__homepage__ = "https://git.sr.ht/~bow/crimson"
__version__ = get_version(__name__, Path(__file__).parent.parent)

del Path, get_version
