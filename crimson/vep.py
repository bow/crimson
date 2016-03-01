# -*- coding: utf-8 -*-
"""
    crimson.vep
    ~~~~~~~~~~~

    VEP plain text statistics file output parsing.

    :copyright: (c) 2016 Wibowo Arindrarto <bow@bow.web.id>
    :license: BSD

"""
from .utils import get_handle


__all__ = ["parse"]


# Default maximum file size ~ because our parser is not a streaming parser.
_MAX_SIZE = 1024 * 500  # 500 Kb


def group2entry(group):
    """Given a VEP statistics group, return it as a tuple suitable
    for creating the payload dictionary."""


def parse(in_data, max_size=_MAX_SIZE):
    """Parses a VEP plain text statistics file into a dictionary.

    :param in_data: Input VEP statistics contents.
    :type in_data: str or file handle
    :param max_size: Maximum expected size of input contents.
    :type max_size: int
    :returns: Parsed VEP statistics values.
    :rtype: dict

    """
    with get_handle(in_data) as fh:
        contents = fh.read(max_size)

    payload = {}
    groups = contents.split("\n\n")

    payload = {k: v for group in groups
               for k, v in group2entry(group)}

    return payload
