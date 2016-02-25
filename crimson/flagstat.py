# -*- coding: utf-8 -*-
"""
    crimson.flagstat
    ~~~~~~~~~~~~~~~~

    Samtools flagstat output parsing.

    :copyright: (c) 2015 Wibowo Arindrarto <bow@bow.web.id>
    :license: BSD

"""
import re
from functools import partial

import click

from .utils import get_handle


__all__ = ["parse"]


_MAX_SIZE = 1024 * 10
_RE_TOTAL = re.compile(r"(\d+) \+ (\d+) in total")
_RE_DUPLICATES = re.compile(r"(\d+) \+ (\d+) duplicates")
_RE_SECONDARY = re.compile(r"(\d+) \+ (\d+) secondary")
_RE_SUPPLIMENTARY = re.compile(r"(\d+) \+ (\d+) supplimentary")
_RE_MAPPED = re.compile(r"(\d+) \+ (\d+) mapped ")
_RE_PAIRED_SEQ = re.compile(r"(\d+) \+ (\d+) paired in ")
_RE_READ1 = re.compile(r"(\d+) \+ (\d+) read1")
_RE_READ2 = re.compile(r"(\d+) \+ (\d+) read2")
_RE_PAIRED_PROPER = re.compile(r"(\d+) \+ (\d+) properly")
_RE_PAIRED_BAM = re.compile(r"(\d+) \+ (\d+) with itself and")
_RE_SINGLETON = re.compile(r"(\d+) \+ (\d+) singletons")
_RE_DIFF = re.compile(r"(\d+) \+ (\d+) with mate mapped "
                      "to a different chr\s\d")
_RE_DIFF_MIN = re.compile(r"(\d+) \+ (\d+) with mate mapped "
                          "to a different chr\s\(")


def search(text, pattern, caster=str):
    """Searches a text for a pattern and returns the results as the given type.

    :param text: Text to search against.
    :type text: str.
    :param pattern: Compiled regular expression.
    :type pattern: pattern object.
    :param caster: One-argument function that is applied to each search result.
    :type caster: function with one argument.
    :returns: A list of search results.

    """
    search_result = pattern.search(text)
    if search_result is not None:
        return [caster(x) for x in search_result.groups()]
    return [None] * pattern.groups


def parse(in_data):
    """Parses a samtools flagstat result into a dictionary.

    :param in_data: Input flagstat contents.
    :type in_data: str or file handle
    :returns: Parsed flagstat values.
    :rtype: dict

    """
    with get_handle(in_data) as fh:
        contents = fh.read(_MAX_SIZE)

    f = partial(search, contents, caster=int)
    parsed = (
        ("total", f(_RE_TOTAL)),
        ("duplicates", f(_RE_DUPLICATES)),
        ("secondary", f(_RE_SECONDARY)),
        ("supplimentary", f(_RE_SUPPLIMENTARY)),
        ("mapped", f(_RE_MAPPED)),
        ("paired_sequencing", f(_RE_PAIRED_SEQ)),
        ("paired", f(_RE_PAIRED_BAM)),
        ("paired_proper", f(_RE_PAIRED_PROPER)),
        ("read1", f(_RE_READ1)),
        ("read2", f(_RE_READ2)),
        ("singleton", f(_RE_SINGLETON)),
        ("diff_chrom", f(_RE_DIFF)),
        ("diff_chrom_mapq", f(_RE_DIFF_MIN)),
    )
    payload = {
        "pass_qc": {k: v[0] for k, v in parsed if v[0] is not None},
        "fail_qc": {k: v[1] for k, v in parsed if v[1] is not None},
    }
    if len(payload["pass_qc"]) == 0 and len(payload["fail_qc"]) == 0:
        raise click.BadParameter("Cannot parse input flagstat file.")

    return payload
