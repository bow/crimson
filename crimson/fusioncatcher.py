# -*- coding: utf-8 -*-
"""
    crimson.fusioncatcher
    ~~~~~~~~~~~~~~~~~~~~~

    FusionCatcher output parsing.

"""
# (c) 2015-2020 Wibowo Arindrarto <bow@bow.web.id>

from os import PathLike
from typing import Dict, List, TextIO, Union

import click

from .utils import get_handle

__all__ = ["parse"]

# Expected column names
_COLS = {
    "0.99.5a": [
        "Gene_1_symbol(5end_fusion_partner)",
        "Gene_2_symbol(3end_fusion_partner)",
        "Fusion_description", "Counts_of_common_mapping_reads",
        "Spanning_pairs", "Spanning_unique_reads", "Longest_anchor_found",
        "Fusion_finding_method",
        "Fusion_point_for_gene_1(5end_fusion_partner)",
        "Fusion_point_for_gene_2(3end_fusion_partner)",
        "Gene_1_id(5end_fusion_partner)", "Gene_2_id(3end_fusion_partner)",
        "Exon_1_id(5end_fusion_partner)", "Exon_2_id(3end_fusion_partner)",
        "Fusion_sequence", "Predicted_effect", "Predicted_fused_transcripts",
        "Predicted_fused_proteins",
    ],
    "1.00": [
        "Gene_1_symbol(5end_fusion_partner)",
        "Gene_2_symbol(3end_fusion_partner)",
        "Fusion_description",
        "Counts_of_common_mapping_reads",
        "Spanning_pairs",
        "Spanning_unique_reads",
        "Longest_anchor_found",
        "Fusion_finding_method",
        "Fusion_point_for_gene_1(5end_fusion_partner)",
        "Fusion_point_for_gene_2(3end_fusion_partner)",
        "Gene_1_id(5end_fusion_partner)",
        "Gene_2_id(3end_fusion_partner)",
        "Exon_1_id(5end_fusion_partner)",
        "Exon_2_id(3end_fusion_partner)",
        "Fusion_sequence",
        "Predicted_effect"
    ]
}

# Delimiter strings
_DELIM: Dict[str, str] = {
    # Fusion description
    "desc": ",",
    # Chromosome-coordinate-strand
    "loc": ":",
    # Others
    "gen": ";",
}


def parse_lr_entry(
    lr_gene: str,
    lr_brkpoint: str,
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


def split_filter(string: str, delim: str) -> List[str]:
    """Split the given string with the given delimiter.

    If the given string is empty, an empty list is returned.

    :param string: String to split.
    :param delim: Delimiter character.

    """
    if not string:
        return []
    return string.split(delim)


def parse_raw_line(raw_line: str, colnames: List[str]) -> dict:
    """Parse a single line into a dictionary.

    :param raw_line: FusionCatcher result line.
    :param colnames: Column names present in the file.

    """
    values = raw_line.split("\t")
    if len(values) != len(colnames):
        msg = "Line values {0} does not match column names {1}."
        raise click.BadParameter(msg.format(values, colnames))

    d = {k: v.strip() for k, v in zip(colnames, values)}

    f5 = d["Fusion_point_for_gene_1(5end_fusion_partner)"].split(_DELIM["loc"])
    f3 = d["Fusion_point_for_gene_2(3end_fusion_partner)"].split(_DELIM["loc"])

    res = {
        "5end": {
            "geneSymbol": d["Gene_1_symbol(5end_fusion_partner)"],
            "geneID": d["Gene_1_id(5end_fusion_partner)"],
            "exonID": d["Exon_1_id(5end_fusion_partner)"] or None,
            "chromosome": f5[0],
            "position": int(f5[1]),
            "strand": f5[2],
        },
        "3end": {
            "geneSymbol": d["Gene_2_symbol(3end_fusion_partner)"],
            "geneID": d["Gene_2_id(3end_fusion_partner)"],
            "exonID": d["Exon_2_id(3end_fusion_partner)"] or None,
            "chromosome": f3[0],
            "position": int(f3[1]),
            "strand": f3[2],
        },
        "fusionDescription":
            split_filter(d["Fusion_description"], _DELIM["desc"]),
        "nCommonMappingReads": int(d["Counts_of_common_mapping_reads"]),
        "nSpanningPairs": int(d["Spanning_pairs"]),
        "nSpanningUniqueReads": int(d["Spanning_unique_reads"]),
        "longestAnchorLength": int(d["Longest_anchor_found"]),
        "fusionFindingMethod":
            split_filter(d["Fusion_finding_method"], _DELIM["gen"]),
        "fusionSequence": d["Fusion_sequence"],
        "predictedEffect": d["Predicted_effect"],
    }

    # Does predicted_fused_transcripts exist for the column format
    if "Predicted_fused_transcripts" in d:
        FusedTranscripts = split_filter(
            d["Predicted_fused_transcripts"], _DELIM["gen"]
        )
        res["predictedFusedTranscripts"] = FusedTranscripts

    if "Predicted_fused_proteins" in d:
        FusedProteins = split_filter(
            d["Predicted_fused_proteins"], _DELIM["gen"]
        )
        res["predictedFusedProteins"] = FusedProteins

    return res


def parse(in_data: Union[str, PathLike, TextIO]) -> List[dict]:
    """Parse the abridged output of a FusionCatcher run.

    :param in_data: Input FusionCatcher contents.
    :returns: Parsed values.

    """
    payload = []
    with get_handle(in_data) as src:
        first_line = src.readline().strip()
        # Parse column names
        colnames = first_line.split("\t")

        # If none of the colnames are recognised
        if not any(colnames == cols for cols in _COLS.values()):
            msg = "Unexpected column names: {0}."
            raise click.BadParameter(msg.format(colnames))

        for line in src:
            parsed = parse_raw_line(line, colnames)
            payload.append(parsed)

    return payload
