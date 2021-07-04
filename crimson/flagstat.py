"""Parser for samtools flagstat output"""
# (c) 2015-2021 Wibowo Arindrarto <contact@arindrarto.dev>

import re
from functools import partial
from os import PathLike
from typing import List, Optional, Pattern, TextIO, Union

import click

from .utils import get_handle

__all__ = ["parse"]


_MAX_SIZE = 1024 * 10
_RE_TOTAL = re.compile(r"(\d+) \+ (\d+) in total")
_RE_DUPLICATES = re.compile(r"(\d+) \+ (\d+) duplicates")
_RE_SECONDARY = re.compile(r"(\d+) \+ (\d+) secondary")
_RE_SUPPLEMENTARY = re.compile(r"(\d+) \+ (\d+) suppl[ie]mentary")
_RE_MAPPED = re.compile(r"(\d+) \+ (\d+) mapped ")
_RE_PAIRED_SEQ = re.compile(r"(\d+) \+ (\d+) paired in ")
_RE_READ1 = re.compile(r"(\d+) \+ (\d+) read1")
_RE_READ2 = re.compile(r"(\d+) \+ (\d+) read2")
_RE_PAIRED_PROPER = re.compile(r"(\d+) \+ (\d+) properly")
_RE_PAIRED_BAM = re.compile(r"(\d+) \+ (\d+) with itself and")
_RE_SINGLETON = re.compile(r"(\d+) \+ (\d+) singletons")
_RE_DIFF = re.compile(r"(\d+) \+ (\d+) with mate mapped to a different chr\s\d")
_RE_DIFF_MIN = re.compile(r"(\d+) \+ (\d+) with mate mapped to a different chr\s\(")


def search(
    text: str,
    pattern: Pattern,
) -> List[Optional[int]]:
    """Search a text for a pattern and returns the results as integers.

    :param text: Text to search against.
    :param pattern: Compiled regular expression.
    :param caster: One-argument function that is applied to each search result.
    :returns: A list of search results.

    """
    search_result = pattern.search(text)
    if search_result is not None:
        return [int(x) for x in search_result.groups()]
    return [None] * pattern.groups


def parse(in_data: Union[str, PathLike, TextIO], max_size: int = _MAX_SIZE) -> dict:
    """Parse a samtools flagstat result into a dictionary.

    :param in_data: Input flagstat contents.
    :param max_size: Maximum allowed size of the flagstat file (default: 10
        KiB).
    :returns: Parsed flagstat values.

    """
    with get_handle(in_data) as fh:
        contents = fh.read(max_size)

    f = partial(search, contents)
    parsed = (
        ("total", f(_RE_TOTAL)),
        ("duplicates", f(_RE_DUPLICATES)),
        ("secondary", f(_RE_SECONDARY)),
        ("supplementary", f(_RE_SUPPLEMENTARY)),
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
