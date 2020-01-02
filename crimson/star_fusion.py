# -*- coding: utf-8 -*-
"""
    crimson.star_fusion
    ~~~~~~~~~~~~~~~~~~~

    STAR-Fusion output parsing.

"""
# (c) 2015-2020 Wibowo Arindrarto <bow@bow.web.id>

from os import PathLike
from typing import List, TextIO, Union

import click

from .utils import get_handle

__all__ = ["parse"]

# Expected column names
# Abridged column names
_ABR_COLS = [
    "fusion_name", "JunctionReads", "SpanningFrags", "Splice_type",
    "LeftGene", "LeftBreakpoint",
    "RightGene", "RightBreakpoint",
]
# Non-abridged column names
_NONABR_COLS = [
    "fusion_name", "JunctionReads", "SpanningFrags", "Splice_type",
    "LeftGene", "LeftBreakpoint",
    "RightGene", "RightBreakpoint",
    "JunctionReads", "SpanningFrags",
]

# Delimiter strings
_DELIM = {
    # Gene name-id
    "gids": "^",
    # Chromosome-coordinate-strand
    "loc": ":",
}


def parse_lr_entry(lr_gene: str, lr_brkpoint: str) -> dict:
    """Parse the gene and breakpoint entry.

    :param lr_gene: Column value for 'LeftGene' or 'RightGene'.
    :param lr_brkpoint: Column value for 'LeftBreakpoint' or 'RightBreakpoint'.

    """
    lrgname, lrgid = lr_gene.split(_DELIM["gids"])
    lrchrom, lrpos, lrstrand = lr_brkpoint.split(_DELIM["loc"])

    return {
        "geneName": lrgname,
        "geneID": lrgid,
        "chromosome": lrchrom,
        "position": int(lrpos),
        "strand": lrstrand,
    }


def parse_raw_line(
    raw_line: str,
    colnames: List[str],
    is_abridged: bool = True,
) -> dict:
    """Parse a single line into a dictionary.

    :param raw_line: STAR-Fusion result line.
    :param colnames: Column names present in the file.
    :param is_abridged: Whether the input raw line is from an abridged file.

    """
    values = raw_line.split("\t")
    if len(values) != len(colnames):
        msg = "Line values {0} does not match column names {1}."
        raise click.BadParameter(msg.format(values, colnames))

    entries, reads = {}, {}
    if is_abridged:
        entries = {k: v for k, v in zip(colnames, values)}
    else:
        entry_colnames, read_colnames = colnames[:-2], colnames[-2:]
        entry_values, read_values = values[:-2], values[-2:]
        entries = {k: v for k, v in zip(entry_colnames, entry_values)}
        reads = {k: v.split(",") for k, v in zip(read_colnames, read_values)}

    ret = {
        "fusionName": entries["fusion_name"],
        "nJunctionReads": int(entries["JunctionReads"]),
        "nSpanningFrags": int(entries["SpanningFrags"]),
        "spliceType": entries["Splice_type"],
        "left": parse_lr_entry(entries["LeftGene"],
                               entries["LeftBreakpoint"]),
        "right": parse_lr_entry(entries["RightGene"],
                                entries["RightBreakpoint"]),
    }
    if reads:
        ret["reads"] = {
            "junctionReads": reads["JunctionReads"],
            "spanningFrags": reads["SpanningFrags"],
        }

    return ret


def parse(in_data: Union[str, PathLike, TextIO]) -> List[dict]:
    """Parses the abridged output of a STAR-Fusion run.

    :param in_data: Input STAR-Fusion contents.

    """
    payload = []
    with get_handle(in_data) as src:
        first_line = src.readline().strip()
        if not first_line.startswith("#"):
            msg = "Unexpected header line: '{0}'."
            raise click.BadParameter(msg.format(first_line))
        # Parse column names, after removing the '#' character
        colnames = first_line[1:].split("\t")
        if colnames != _ABR_COLS and colnames != _NONABR_COLS:
            msg = "Unexpected column names: {0}."
            raise click.BadParameter(msg.format(colnames))
        else:
            is_abridged = colnames == _ABR_COLS
            for line in (x.strip() for x in src):
                parsed = parse_raw_line(line, colnames, is_abridged)
                payload.append(parsed)

    return payload
