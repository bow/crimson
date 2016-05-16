# -*- coding: utf-8 -*-
"""
    crimson.fusioncatcher
    ~~~~~~~~~~~~~~~~~~~~~

    FusionCatcher output parsing.

    :copyright: (c) 2016 Wibowo Arindrarto <bow@bow.web.id>
    :license: BSD

"""
import click

from .utils import get_handle


__all__ = ["parse"]

# Expected column names
_COLS = [
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
]

# Delimiter strings
_DELIM = {
    # Fusion description
    "desc": ",",
    # Chromosome-coordinate-strand
    "loc": ":",
    # Others
    "gen": ";",
}


def parse_lr_entry(lr_gene, lr_brkpoint):
    """Parses the gene and breakpoint entry.

    :param lr_gene: Column value for 'LeftGene' or 'RightGene'.
    :type lr_gene: str
    :param lr_brkpoint: Column value for 'LeftBreakpoint' or 'RightBreakpoint'.
    :type lr_brkpoint: str
    :rtype: dict

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


def split_filter(string, delim):
    if not string:
        return []
    return string.split(delim)


_COLS = [
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
]


def parse_raw_line(raw_line, colnames=_COLS):
    """Parses a single line into a dictionary.

    :param raw_line: FusionCatcher result line.
    :type raw_line: str
    :param colnames: Column names present in the file.
    :type colnames: list of str
    :rtype: dict

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
        "predictedFusedTranscripts":
            split_filter(d["Predicted_fused_transcripts"], _DELIM["gen"]),
        "predictedFusedProteins":
            split_filter(d["Predicted_fused_proteins"], _DELIM["gen"]),
    }
    return res


def parse(in_data):
    """Parses the abridged output of a FusionCatcher run.

    :param in_data: Input FusionCatcher contents.
    :type in_data: str or file handle
    :returns: Parsed values.
    :rtype: dict

    """
    payload = []
    with get_handle(in_data) as src:
        first_line = src.readline().strip()
        # Parse column names
        colnames = first_line.split("\t")
        if colnames != _COLS:
            msg = "Unexpected column names: {0}."
            raise click.BadParameter(msg.format(colnames))
        for line in (x for x in src):
            parsed = parse_raw_line(line)
            payload.append(parsed)

    return payload
