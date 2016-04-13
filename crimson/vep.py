# -*- coding: utf-8 -*-
"""
    crimson.vep
    ~~~~~~~~~~~

    VEP plain text statistics file output parsing.

    :copyright: (c) 2016 Wibowo Arindrarto <bow@bow.web.id>
    :license: BSD

"""
import click

from .utils import convert, get_handle


__all__ = ["parse"]


# Default maximum file size ~ because our parser is not a streaming parser.
_MAX_SIZE = 1024 * 500  # 500 Kb


def group2entry(group):
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

    values = (line.split("\t", 1) for line in raw_value.strip().split("\n"))

    if not key.startswith("Distribution of variants on"):
        valued = {k: convert(v) for k, v in values}
        return key, valued

    return key, [convert(v) for _, v in values]


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

    if not contents.startswith("[VEP run statistics]"):
        msg = "Unexpected file structure. No contents parsed."
        raise click.BadParameter(msg)

    entries = [group2entry(g) for g in contents.split("\n\n")]
    return dict(entries)
