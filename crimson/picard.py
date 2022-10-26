"""Parser for Picard metrics files"""
# Copyright (c) 2015-2022 Wibowo Arindrarto <contact@arindrarto.dev>
# SPDX-License-Identifier: BSD-3-Clause

import os
import re
from typing import Any, Dict, Optional, TextIO, Union

import click

from .utils import convert, get_handle, get_linesep

_MAX_SIZE = 1024 * 1024 * 1
_RE_HEADER = re.compile(r"^#+\s+")


__all__ = ["parse"]


def parse_header(header: str, linesep: str) -> Dict[str, str]:
    """Parse the Picard header lines into a dictionary.

    :param header: Raw Picard header string.
    :param linesep: Line separator characters used when parsing.

    """
    parsed = [_RE_HEADER.sub("", x) for x in header.split(linesep)]
    if len(parsed) != 4:
        raise ValueError("Unexpected Picard header.")

    return {"flags": parsed[1], "time": parsed[3]}


def parse_metrics(metrics: Optional[str], linesep: str) -> Optional[dict]:
    """Parse the Picard metrics lines into a dictionary.

    :param metris: Raw Picard metrics string.
    :param linesep: Line separator characters used when parsing.

    """
    if metrics is None:
        return None

    lines = [line.strip(linesep) for line in metrics.split(linesep)]

    metrics_class: Optional[str]
    try:
        metrics_class = lines.pop(0).split("\t")[1]
    except IndexError:
        metrics_class = None

    parsed = []
    for line in lines:
        parsed.append([convert(v) for v in line.split("\t")])

    header_cols = parsed.pop(0)
    contents: Any = [dict(zip(header_cols, line)) for line in parsed]
    if len(contents) == 1:
        contents = contents.pop()
    payload: dict = {"contents": contents}
    if metrics_class is not None:
        payload["class"] = metrics_class

    return payload


def parse_histogram(histo: Optional[str], linesep: str) -> Optional[dict]:
    """Parse the Picard histogram lines into a dictionary.

    :param metris: Raw Picard histogram string.
    :param linesep: Line separator characters used when parsing.

    """
    if histo is None:
        return None

    lines = [line.strip(linesep) for line in histo.split(linesep)]
    lines.pop(0)

    parsed = []
    for line in lines:
        parsed.append([convert(v) for v in line.split("\t")])

    header_cols = parsed.pop(0)
    payload = {"contents": [dict(zip(header_cols, line)) for line in parsed]}

    return payload


def parse(
    in_data: Union[str, os.PathLike, TextIO],
    input_linesep: Optional[str] = None,
    max_size: int = _MAX_SIZE,
) -> dict:
    """Parse an input Picard metrics file into a dictionary.

    :param in_data: Input metrics file.
    :param input_linesep: Name of the operating system used for determining
        input line separator. Valid values are 'nt', 'posix', or None.
    :param max_size: Maximum allowed size of the Picard metrics file (default:
        10 MiB).

    """
    with get_handle(in_data) as fh:
        contents = fh.read(max_size)

    linesep = get_linesep(input_linesep)
    sections = contents.strip(linesep).split(linesep * 2)

    header = next((x for x in sections if x.startswith("## htsjdk")), None)
    if header is None:
        raise click.BadParameter("Unexpected Picard metrics file format.")

    metrics = next((x for x in sections if x.startswith("## METRICS")), None)
    histo = next((x for x in sections if x.startswith("## HISTOGRAM")), None)

    return {
        "header": parse_header(header, linesep),
        "metrics": parse_metrics(metrics, linesep),
        "histogram": parse_histogram(histo, linesep),
    }
