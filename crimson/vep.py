# -*- coding: utf-8 -*-
"""
    crimson.vep
    ~~~~~~~~~~~

    VEP plain text statistics file output parsing.

"""
# (c) 2015-2020 Wibowo Arindrarto <bow@bow.web.id>

import collections
from os import PathLike
from typing import Dict, List, TextIO, Tuple, Union

import click

from .utils import convert, get_handle

__all__ = ["parse"]


# Default maximum file size ~ because our parser is not a streaming parser.
_MAX_SIZE = 1024 * 500  # 500 Kb


def parse_raw_value(raw_value):
    """ Parse raw values from VEP """
    parsed = list()
    for line in raw_value.strip().split("\n"):
        # This is the regular case
        if '\t' in line:
            parsed.append(line.split("\t", 1))
        # Special cases where VEP was run on an emtpy input file
        elif line == 'Lines of input read':
            parsed.append(['Lines of input read', '0'])
        elif line == 'Variants processed':
            parsed.append(['Variants processed', '0'])
    return parsed


def group2entry(
    group: str,
) -> Tuple[
    str,
    Union[
        List[Union[str, int, float]],
        Dict[str, Union[str, int, float]],
    ]
]:
    """Given the raw string of a VEP statistics group, parse it into a
    key, value tuple.

    Basically, turning this:

        [Variant classes]
        deletion    18
        insertion   35
        SNV 448

    into this:

        ("Variant classes", {
            "deletion": 18,
            "insertion": 35,
            "SNV": 448
         })

    except for then the VEP group represents a histogram, which is the
    case for groups whose name starts with "Distribution of variants ...".

    Those groups, which may look like this:

        [Distribution of variants on chromosome 1]
        0   1
        1   40
        2   35
        3   50
        ...

    gets turned into this:

        ("Distribution of variants on chromosome 1",
         [1, 40, 35, 50, ...])

    """
    raw_key, raw_value = group.split("\n", 1)
    key = raw_key[1:-1]

    # If there are no values for this section, return a default dict of
    # integers, so that any property a user requests will be 0
    if not raw_value:
        return key, collections.defaultdict(int)

    values = parse_raw_value(raw_value)

    if not key.startswith("Distribution of variants on"):
        valued = {k: convert(v) for k, v in values}
        return key, valued

    return key, [convert(v) for _, v in values]


def parse(
    in_data: Union[str, PathLike, TextIO],
    max_size: int = _MAX_SIZE,
) -> dict:
    """Parse a VEP plain text statistics file into a dictionary.

    :param in_data: Input VEP statistics contents.
    :param max_size: Maximum expected size of input contents (default: 500 KiB).

    """
    with get_handle(in_data) as fh:
        contents = fh.read(max_size)

    if not contents.startswith("[VEP run statistics]"):
        msg = "Unexpected file structure. No contents parsed."
        raise click.BadParameter(msg)

    entries = [group2entry(g) for g in contents.split("\n\n")]

    return dict(entries)
