# -*- coding: utf-8 -*-
"""
    crimson.picard
    ~~~~~~~~~~~~~~

    Picard metrics file parsing.

"""
# (c) 2015-2020 Wibowo Arindrarto <bow@bow.web.id>

import os
import re
from typing import Any, Dict, Optional, TextIO, Union

import click

from .utils import convert, get_handle

_MAX_SIZE = 1024 * 1024 * 1
_RE_HEADER = re.compile(r"^#+\s+")


__all__ = ["parse"]


def parse_header(header: str) -> Dict[str, str]:
    """Parse the Picard header lines into a dictionary.

    :param header: Raw Picard header string.

    """
    parsed = [_RE_HEADER.sub("", x) for x in header.split(os.linesep)]
    if len(parsed) != 4:
        raise ValueError("Unexpected Picard header.")

    return {"flags": parsed[1], "time": parsed[3]}


def parse_metrics(metrics: Optional[str]) -> Optional[dict]:
    """Parse the Picard metrics lines into a dictionary.

    :param metris: Raw Picard metrics string.

    """
    if metrics is None:
        return None

    lines = [l.strip(os.linesep) for l in metrics.split(os.linesep)]

    metrics_class: Optional[str]
    try:
        metrics_class = lines.pop(0).split("\t")[1]
    except IndexError:
        metrics_class = None

    parsed = []
    for line in lines:
        parsed.append([convert(v) for v in line.split("\t")])

    header_cols = parsed.pop(0)
    contents: Any = [dict(zip(header_cols, l)) for l in parsed]
    if len(contents) == 1:
        contents = contents.pop()
    payload: dict = {"contents": contents}
    if metrics_class is not None:
        payload["class"] = metrics_class

    return payload


def parse_histogram(histo: Optional[str]) -> Optional[dict]:
    """Parse the Picard histogram lines into a dictionary.

    :param metris: Raw Picard histogram string.

    """
    if histo is None:
        return None

    lines = [l.strip(os.linesep) for l in histo.split(os.linesep)]
    lines.pop(0)

    parsed = []
    for line in lines:
        parsed.append([convert(v) for v in line.split("\t")])

    header_cols = parsed.pop(0)
    payload = {"contents": [dict(zip(header_cols, l)) for l in parsed]}

    return payload


def parse(
    in_data: Union[str, os.PathLike, TextIO],
    max_size: int = _MAX_SIZE,
) -> dict:
    """Parse an input Picard metrics file into a dictionary.

    :param in_data: Input metrics file.
    :param max_size: Maximum allowed size of the Picard metrics file (default:
        10 MiB).

    """
    with get_handle(in_data) as fh:
        contents = fh.read(max_size)

    sections = contents.strip(os.linesep).split(os.linesep * 2)

    header = next((x for x in sections if x.startswith("## htsjdk")), None)
    if header is None:
        raise click.BadParameter("Unexpected Picard metrics file format.")

    metrics = next((x for x in sections if x.startswith("## METRICS")), None)
    histo = next((x for x in sections if x.startswith("## HISTOGRAM")), None)

    return {
        "header": parse_header(header),
        "metrics": parse_metrics(metrics),
        "histogram": parse_histogram(histo),
    }
