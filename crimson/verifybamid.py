# -*- coding: utf-8 -*-
"""
    crimson.verifybamid
    ~~~~~~~~~~~~~~

    verifyBamId file parsing.

    :copyright: (c) 2017 Dave Larson <delarson@wustl.edu>
    :license: BSD

"""
import re
import os

import click

from .utils import convert, get_handle


__all__ = ["parse"]


def parse(in_data):
    """Parses verifyBamId output into a dictionary.

    :param in_data: Input verifyBamId contents.
    :type in_data: str or file handle
    :returns: Parsed verifyBamId values.
    :rtype: dict

    """

    header_lines = []
    data_lines = []
    with get_handle(in_data) as fh:
        for line in fh:
            if line.startswith('#'):
                header_lines.append(line.rstrip(os.linesep)[1:])
            else:
                data_lines.append(line.rstrip(os.linesep))

    if len(header_lines) == 1:
        header_cols = header_lines[0].split("\t")
    else:
        raise ValueError("Missing verifyBamId header.")

    if data_lines:
        contents = [dict(zip(header_cols, [convert(v) for v in l.split("\t")])) for l in data_lines]

    if len(contents) == 1:
        contents = contents.pop()
    return contents
