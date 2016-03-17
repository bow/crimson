# -*- coding: utf-8 -*-
"""
    crimson.star
    ~~~~~~~~~~~~

    STAR Log.final.out file.

    :copyright: (c) 2016 Wibowo Arindrarto <bow@bow.web.id>
    :license: BSD

"""
import os

import click

from .utils import convert, get_handle


__all__ = ["parse"]


def _pct_convert(raw_str):
    """Converts the given number ending with '%' to a number."""
    if raw_str.endswith("%"):
        return convert(raw_str[:-1])
    return convert(raw_str)


_MAX_SIZE = 1024 * 10
# Mapping of STAR attribute names to python dictionary attribute names
# and the function used to parse it.
_PARSE_MAP = {
    "Started job on":
        ("timeJobStart", str),
    "Started mapping on":
        ("timeMappingStart", str),
    "Finished on":
        ("timeEnd", str),
    "Mapping speed, Million of reads per hour":
        ("mappingSpeed", convert),
    "Number of input reads":
        ("nInput", convert),
    "Average input read length":
        ("avgInputLength", convert),
    "Uniquely mapped reads number":
        ("nUniquelyMapped", convert),
    "Uniquely mapped reads %":
        ("pctUniquelyMapped", _pct_convert),
    "Average mapped length":
        ("avgMappedLength", convert),
    "Number of splices: Total":
        ("nSplicesTotal", convert),
    "Number of splices: Annotated (sjdb)":
        ("nSplicesAnnotated", convert),
    "Number of splices: GT/AG":
        ("nSplicesGTAG", convert),
    "Number of splices: GC/AG":
        ("nSplicesGCAG", convert),
    "Number of splices: AT/AC":
        ("nSplicesATAC", convert),
    "Number of splices: Non-canonical":
        ("nSplicesNonCanonical", convert),
    "Mismatch rate per base, %":
        ("rateMismatchPerBase", _pct_convert),
    "Deletion rate per base":
        ("rateDeletionPerBase", _pct_convert),
    "Deletion average length":
        ("avgDeletionLength", convert),
    "Insertion rate per base":
        ("rateInsertionPerBase", _pct_convert),
    "Insertion average length":
        ("avgInsertionLength", convert),
    "Number of reads mapped to multiple loci":
        ("nMappedMultipleLoci", convert),
    "% of reads mapped to multiple loci":
        ("pctMappedMultipleLoci", _pct_convert),
    "Number of reads mapped to too many loci":
        ("nMappedTooManyLoci", convert),
    "% of reads mapped to too many loci":
        ("pctMappedTooManyLoci", _pct_convert),
    "% of reads unmapped: too many mismatches":
        ("pctUnmappedForTooManyMismatches", _pct_convert),
    "% of reads unmapped: too short":
        ("pctUnmappedForTooShort", _pct_convert),
    "% of reads unmapped: other":
        ("pctUnmappedForOther", _pct_convert),
}


def parse(in_data):
    """Parses the log of a STAR run.

    :param in_data: Input STAR-Fusion contents.
    :type in_data: str or file handle
    :returns: Parsed values.
    :rtype: dict

    """
    payload = {}
    with get_handle(in_data) as src:
        contents = src.read(_MAX_SIZE)

    for line in contents.split(os.linesep):
        # pass empty lines
        if line and not line.strip():
            continue
        line = line.strip()
        if '|' in line:
            ori_key, val = [x.strip() for x in line.split('|', 1)]
            if ori_key in _PARSE_MAP:
                key, func = _PARSE_MAP[ori_key]
                val = func(val)
                if key in payload:
                    msg = "Unexpected duplicate key entry: {0} ({1})."
                    raise click.BadParameter(msg.format(key, ori_key))
                payload[key] = val

    if not payload:
        msg = "Unexpected file structure. No contents parsed."
        raise click.BadParameter(msg)
    return payload
