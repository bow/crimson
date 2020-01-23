# -*- coding: utf-8 -*-
"""
    crimson.star_fusion
    ~~~~~~~~~~~~~~~~~~~

    STAR-Fusion output parsing.

"""
# (c) 2015-2020 Wibowo Arindrarto <bow@bow.web.id>

from os import PathLike
from typing import Any, Dict, List, TextIO, Tuple, Union

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

# Non-abridged column names star-fusion 1.6.0
_NONABR_COLS_v160 = [
    "FusionName", "JunctionReadCount", "SpanningFragCount", "SpliceType",
    "LeftGene", "LeftBreakpoint", "RightGene", "RightBreakpoint",
    "JunctionReads", "SpanningFrags", "LargeAnchorSupport", "FFPM",
    "LeftBreakDinuc", "LeftBreakEntropy", "RightBreakDinuc",
    "RightBreakEntropy", "annots"
]

# Supported columns
SUPPORTED = {
    'v1.6.0': _NONABR_COLS_v160,
    'v0.6.0': _NONABR_COLS,
    'v0.6.0_abr': _ABR_COLS
}

# Special columns, currently shared by all output formats
# These have to be parsed in special way
SPECIAL = ["LeftGene", "LeftBreakpoint", "RightGene", "RightBreakpoint"]

# Mapping of supported columns to output format
#
# Column name in file -> field name in json
#
# Note: the JunctionReads and SpanningFrags columns are present twice in
# the output files, with different meanings and content
# SPECIAL columns are excluded
COL_MAPPING = {
    'v0.6.0': {
        'fusion_name': 'fusionName',
        'JunctionReads': 'nJunctionReads',
        'SpanningFrags': 'nSpanningFrags',
        'Splice_type': 'spliceType'
    },
    'v0.6.0_abr': {
        'fusion_name': 'fusionName',
        'JunctionReads': 'nJunctionReads',
        'SpanningFrags': 'nSpanningFrags',
        'Splice_type': 'spliceType'
    },
    'v1.6.0': {
        'FusionName': 'fusionName',
        'JunctionReadCount': 'nJunctionReads',
        'SpanningFragCount': 'nSpanningFrags',
        'SpliceType': 'spliceType',
        'JunctionReads': 'junctionReads',
        'SpanningFrags': 'spanningFrags',
        'LargeAnchorSupport': 'largeAnchorSupport',
        'FFPM': 'FFPM',
        'LeftBreakDinuc': 'leftBreakDinuc',
        'LeftBreakEntropy': 'leftBreakEntropy',
        'RightBreakDinuc': 'rightBreakDinuc',
        'RightBreakEntropy': 'rightBreakEntropy',
        'annots': 'annots'
    }
}

# Delimiter strings
_DELIM = {
    # Gene name-id
    "gids": "^",
    # Chromosome-coordinate-strand
    "loc": ":",
}


def parse_lr_entry(
    lr_gene: str,
    lr_brkpoint: str
) -> Dict[str, Union[str, int]]:
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


def parse_read_columns(
    colnames: List[str],
    values: List[str]
) -> Tuple[Dict[str, str], Dict[str, List[str]]]:
    """Parse the read columns out and return them seperately

    The JunctionReads and SpanningFrags columns can contain the actual reads,
    or just the counts of the reads. This makes parsing them correctly quite
    convoluted.

    Assumption: The last occurrence of the JunctionReads and SpanningFrags
    columns in the file contain the actual reads, while the first one contains
    the counts.
    If there is only one (as is the case for v1.6.0), it contains the reads

    :param values: List of values from the file
    :para colnames: List of column names from the file
    """
    entries = dict()
    reads = dict()

    # Keep the column names and values together
    together = [(name, val) for name, val in zip(colnames, values)]

    # Extract the JunctionReads
    rev = together[::-1]
    for name, val in rev:
        if name == 'JunctionReads':
            together.remove((name, val))
            break
    reads[name] = val.split(',')

    # Extract the SpanningFrags
    for name, val in rev:
        if name == 'SpanningFrags':
            together.remove((name, val))
            break
    reads[name] = val.split(',')

    # The other columns are regular entries
    entries = {k: v for k, v in together}

    return entries, reads


def parse_raw_line(
    raw_line: str,
    version: str,
    is_abridged: bool = True,
) -> Dict[str, Any]:
    """Parse a single line into a dictionary.

    :param raw_line: STAR-Fusion result line.
    :param version: The version of the output format present in the file.
    :param is_abridged: Whether the input raw line is from an abridged file.

    """
    values = raw_line.split("\t")
    colnames = SUPPORTED[version]

    if len(values) != len(colnames):
        msg = "Line values {0} does not match column names {1}."
        raise click.BadParameter(msg.format(values, colnames))

    if is_abridged:
        entries = {k: v for k, v in zip(colnames, values)}
        reads = dict()  # type: Dict[str, List[str]]
    else:
        # If the format is not abridged, the JunctionReads and SpanningFrags
        # columns are duplicated
        entries, reads = parse_read_columns(colnames, values)

    # Create the output dictionary based on the detected star-fusion version
    ret = dict()  # type: Dict[str, Any]
    for colname in entries:
        if colname in SPECIAL:
            continue
        field_name = COL_MAPPING[version][colname]
        ret[field_name] = entries[colname]

    # Cast the apropriate entries to int
    # These values should always exist
    for int_field in ['nJunctionReads', 'nSpanningFrags']:
        ret[int_field] = int(ret[int_field])

    # Cast the apropriate entries to float
    # These values can be missing
    for float_field in ['FFPM', 'leftBreakEntropy', 'rightBreakEntropy']:
        try:
            ret[float_field] = float(ret[float_field])
        except KeyError:
            continue

    # Handle the SPECIAL columns
    ret["left"] = parse_lr_entry(entries["LeftGene"],
                                 entries["LeftBreakpoint"])
    ret["right"] = parse_lr_entry(entries["RightGene"],
                                  entries["RightBreakpoint"])

    if reads:
        ret["reads"] = {
            "junctionReads": reads["JunctionReads"],
            "spanningFrags": reads["SpanningFrags"],
        }

    return ret


def detect_format(colnames: List[str]) -> str:
    """ Return the detected column format """
    for colformat in SUPPORTED:
        if SUPPORTED[colformat] == colnames:
            return colformat
    else:
        msg = "Unexpected column names: {0}."
        raise click.BadParameter(msg.format(colnames))


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
        version = detect_format(colnames)
        is_abridged = version == 'v0.6.0_abr'
        for line in (x.strip() for x in src):
            parsed = parse_raw_line(line, version, is_abridged)
            payload.append(parsed)

    return payload
