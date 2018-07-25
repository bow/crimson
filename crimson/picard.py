# -*- coding: utf-8 -*-
"""
    crimson.picard
    ~~~~~~~~~~~~~~

    Picard metrics file parsing.

"""
# (c) 2015-2018 Wibowo Arindrarto <bow@bow.web.id>
import os
import re

import click

from .utils import convert, get_handle


_MAX_SIZE = 1024 * 1024 * 1
_RE_HEADER = re.compile(r"^#+\s+")


__all__ = ["parse"]


def fetch(l, pred, first=True):
    """Fetches item(s) that return true in the given list.

    :param l: Input list to fetch from.
    :type l: list
    :param pred: Predicate function.
    :type pred: function
    :param first: Whether to return only the first matching item or
                  all matching items.
    :type first: bool

    """
    matches = [x for x in l if pred(x)]
    if len(matches) == 0:
        return None
    if first:
        return matches[0]
    return matches


def parse_header(header):
    """Parses the Picard header lines into a dictionary.

    :param header: Raw Picard header string.
    :type header: str
    :returns: Parsed header information.
    :rtype: dict

    """
    parsed = [_RE_HEADER.sub("", x) for x in header.split(os.linesep)]
    if len(parsed) != 4:
        raise ValueError("Unexpected Picard header.")

    return {"flags": parsed[1], "time": parsed[3]}


def parse_metrics(metrics):
    """Parses the Picard metrics lines into a dictionary.

    :param metris: Raw Picard metrics string.
    :type metrics: str
    :returns: Parsed metrics table.
    :rtype: dict

    """
    if metrics is None:
        return

    lines = [l.strip(os.linesep) for l in metrics.split(os.linesep)]

    try:
        metrics_class = lines.pop(0).split("\t")[1]
    except IndexError:
        metrics_class = None

    parsed = []
    for line in lines:
        parsed.append([convert(v) for v in line.split("\t")])

    header_cols = parsed.pop(0)
    contents = [dict(zip(header_cols, l)) for l in parsed]
    if len(contents) == 1:
        contents = contents.pop()
    payload = {"contents": contents}
    if metrics_class is not None:
        payload["class"] = metrics_class

    return payload


def parse_histogram(histo):
    """Parses the Picard histogram lines into a dictionary.

    :param metris: Raw Picard histogram string.
    :type metrics: str
    :returns: Parsed histogram table.
    :rtype: dict

    """
    if histo is None:
        return

    lines = [l.strip(os.linesep) for l in histo.split(os.linesep)]
    lines.pop(0)

    parsed = []
    for line in lines:
        parsed.append([convert(v) for v in line.split("\t")])

    header_cols = parsed.pop(0)
    payload = {"contents": [dict(zip(header_cols, l)) for l in parsed]}

    return payload


def parse(in_data, max_size=_MAX_SIZE):
    """Parses an input Picard metrics file into a dictionary.

    :param in_data: Input metrics file.
    :type in_data: str or file handle
    :param max_size: Maximum allowed size of the Picard metrics file
                     (default: 10 MiB).
    :type max_size: int
    :returns: Parsed metrics values.
    :rtype: dict

    """
    with get_handle(in_data) as fh:
        contents = fh.read(max_size)

    sections = contents.strip(os.linesep).split(os.linesep * 2)

    header = fetch(sections, lambda x: x.startswith("## htsjdk"))
    if header is None:
        raise click.BadParameter("Unexpected Picard metrics file format.")
    metrics = fetch(sections, lambda x: x.startswith("## METRICS"))
    histo = fetch(sections, lambda x: x.startswith("## HISTOGRAM"))

    return {
        "header": parse_header(header),
        "metrics": parse_metrics(metrics),
        "histogram": parse_histogram(histo),
    }
