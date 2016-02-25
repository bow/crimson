# -*- coding: utf-8 -*-
"""
    crimson.star_fusion
    ~~~~~~~~~~~~~~~~~~~

    STAR-Fusion abridged output parsing.

    :copyright: (c) 2016 Wibowo Arindrarto <bow@bow.web.id>
    :license: BSD

"""
import click

from .utils import get_handle


__all__ = ["parse"]

# Expected column names
_COLNAMES = [
    "fusion_name", "JunctionReads", "SpanningFrags", "Splice_type",
    "LeftGene", "LeftBreakpoint",
    "RightGene", "RightBreakpoint",
]

# Delimiter strings
_DELIM = {
    # Fusion gene names
    "fusn": "--",
    # Gene-transcript name
    "gtrans": "^",
    # Chromosome-coordinate-strand
    "loc": ":",
}


def parse_lr_entry(lr_gene, lr_brkpoint):
    """Parses the gene and breakpoint entry.

    :param lr_gene: Column value for 'LeftGene' or 'RightGene'.
    :type lr_gene: str
    :param lr_brkpoint: Column value for 'LeftBreakpoint' or 'RightBreakpoint'.
    :type lr_brkpoint: str
    :rtype: dict

    """
    lrgene, lrtrans = lr_gene.split(_DELIM["gtrans"])
    lrchrom, lrcoord, lrstrand = lr_brkpoint.split(_DELIM["loc"])

    return {
        "gene": lrgene,
        "transcript": lrtrans,
        "chromosome": lrchrom,
        "coordinate": int(lrcoord),
        "strand": lrstrand,
    }


def parse_raw_line(raw_line, colnames):
    """Parses a single line into a dictionary.

    :param raw_line: STAR-Fusion result line.
    :type raw_line: str
    :param colnames: Column names present in the file.
    :type colnames: list of str
    :rtype: dict

    """
    values = raw_line.split("\t")
    if len(values) != len(colnames):
        msg = "Line values {0} does not match column names {1}."
        raise click.BadParameter(msg.format(values, colnames))
    entries = {k: v for k, v in zip(colnames, values)}

    return {
        "name": entries["fusion_name"],
        "nJunctionReads": int(entries["JunctionReads"]),
        "nSpanningFrags": int(entries["SpanningFrags"]),
        "spliceType": entries["Splice_type"],
        "left": parse_lr_entry(entries["LeftGene"],
                               entries["LeftBreakpoint"]),
        "right": parse_lr_entry(entries["RightGene"],
                                entries["RightBreakpoint"]),
    }


def parse(in_data):
    """Parses the abridged output of a STAR-Fusion run.

    :param in_data: Input STAR-Fusion contents.
    :type in_data: str or file handle
    :returns: Parsed values.
    :rtype: dict

    """
    payload = []
    with get_handle(in_data) as src:
        first_line = src.readline().strip()
        if not first_line.startswith("#"):
            msg = "Unexpected header line: '{0}'."
            raise click.BadParameter(msg.format(first_line))
        # Parse column names, after removing the '#' character
        colnames = first_line[1:].split("\t")
        if not colnames == _COLNAMES:
            msg = "Unexpected column names: {0}."
            raise click.BadParameter(msg.format(colnames))
        for line in (x.strip() for x in src):
            parsed = parse_raw_line(line, colnames)
            payload.append(parsed)

    return payload
