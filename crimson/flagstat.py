# -*- coding: utf-8 -*-
"""
    crimson.flagstat
    ~~~~~~~~~~~~~~~~

    Flagstat subcommand.

    :copyright: (c) 2015 Wibowo Arindrarto <bow@bow.web.id>
    :license: BSD

"""
import json
import re
from functools import partial
from os import linesep

import click


__all__ = ["flagstat"]


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


@click.argument("input", type=click.File("r"))
@click.argument("output", type=click.File("w"))
@click.pass_context
def flagstat(ctx, input, output):
    """Converts samtools flagstat output.

    Use "-" for stdin and/or stdout.

    """
    contents = input.read()
    search_contents = partial(search, contents)
    parsed = (
        ("total", search_contents(_RE_TOTAL, int)),
        ("duplicates", search_contents(_RE_DUPLICATES, int)),
        ("secondary", search_contents(_RE_SECONDARY, int)),
        ("supplimentary", search_contents(_RE_SUPPLIMENTARY, int)),
        ("mapped", search_contents(_RE_MAPPED, int)),
        ("paired_sequencing", search_contents(_RE_PAIRED_SEQ, int)),
        ("paired", search_contents(_RE_PAIRED_BAM, int)),
        ("paired_proper", search_contents(_RE_PAIRED_PROPER, int)),
        ("read1", search_contents(_RE_READ1, int)),
        ("read2", search_contents(_RE_READ2, int)),
        ("singleton", search_contents(_RE_SINGLETON, int)),
        ("diff_chrom", search_contents(_RE_DIFF, int)),
        ("diff_chrom_mapq", search_contents(_RE_DIFF_MIN, int)),
    )
    payload = {
        "pass_qc": {k: v[0] for k, v in parsed if v[0] is not None},
        "fail_qc": {k: v[1] for k, v in parsed if v[1] is not None},
    }
    if ctx.parent.params["compact"]:
        json.dump(payload, output, indent=None, separators=(",", ":"))
    else:
        json.dump(payload, output, indent=4)
        output.write(linesep)
