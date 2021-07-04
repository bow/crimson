"""star-fusion subcommand tests"""
# (c) 2015-2021 Wibowo Arindrarto <contact@arindrarto.dev>

import json

import pytest
from click import BadParameter
from click.testing import CliRunner

from crimson.cli import main
from crimson.star_fusion import (
    detect_format,
    parse_annots,
    parse_lr_entry,
    parse_raw_line,
)
from .utils import get_test_path, getattr_nested


@pytest.fixture(scope="module")
def star_fusion_fail():
    runner = CliRunner()
    in_file = get_test_path("star_fusion_nope.txt")
    result = runner.invoke(main, ["star-fusion", in_file])
    return result


@pytest.fixture(scope="module")
def star_fusion_v060_01():
    runner = CliRunner()
    in_file = get_test_path("star_fusion_v060_01.txt")
    result = runner.invoke(main, ["star-fusion", in_file])
    result.json = json.loads(result.output)
    return result


@pytest.fixture(scope="module")
def star_fusion_v060_02():
    runner = CliRunner()
    in_file = get_test_path("star_fusion_v060_02.txt")
    result = runner.invoke(main, ["star-fusion", in_file])
    result.json = json.loads(result.output)
    return result


@pytest.fixture(scope="module")
def star_fusion_v160_dummy():
    runner = CliRunner()
    in_file = get_test_path("star_fusion_v160_dummy.txt")
    result = runner.invoke(main, ["star-fusion", in_file])
    result.json = json.loads(result.output)
    return result


@pytest.fixture(scope="module")
def star_fusion_v160_abr_dummy():
    runner = CliRunner()
    in_file = get_test_path("star_fusion_v160_abr_dummy.txt")
    result = runner.invoke(main, ["star-fusion", in_file])
    result.json = json.loads(result.output)
    return result


@pytest.fixture(scope="module")
def star_fusion_v160_NB4():
    runner = CliRunner()
    in_file = get_test_path("star_fusion_v160_NB4.txt")
    result = runner.invoke(main, ["star-fusion", in_file])
    result.json = json.loads(result.output)
    return result


@pytest.fixture(scope="module")
def star_fusion_v160_abr_NB4():
    runner = CliRunner()
    in_file = get_test_path("star_fusion_v160_abr_NB4.txt")
    result = runner.invoke(main, ["star-fusion", in_file])
    result.json = json.loads(result.output)
    return result


def test_star_fusion_fail_exit_code(star_fusion_fail):
    assert star_fusion_fail.exit_code != 0


def test_star_fusion_fail_output(star_fusion_fail):
    err_msg = "Unexpected header line:"
    assert err_msg in star_fusion_fail.output


@pytest.mark.parametrize(
    "attrs, exp",
    [
        ([0, "fusionName"], "RUNX1--RUNX1T1"),
        ([0, "nJunctionReads"], 30),
        ([0, "nSpanningFrags"], 8),
        ([0, "spliceType"], "ONLY_REF_SPLICE"),
        ([0, "left", "geneName"], "RUNX1"),
        ([0, "left", "geneID"], "ENSG00000159216.18"),
        ([0, "left", "chromosome"], "chr21"),
        ([0, "left", "position"], 34859474),
        ([0, "left", "strand"], "-"),
        ([0, "right", "geneName"], "RUNX1T1"),
        ([0, "right", "geneID"], "ENSG00000079102.16"),
        ([0, "right", "chromosome"], "chr8"),
        ([0, "right", "position"], 92017363),
        ([0, "right", "strand"], "-"),
        ([-1, "fusionName"], "ITM2C--PTMA"),
        ([-1, "nJunctionReads"], 1),
        ([-1, "nSpanningFrags"], 1),
        ([-1, "spliceType"], "ONLY_REF_SPLICE"),
        ([-1, "left", "geneName"], "ITM2C"),
        ([-1, "left", "geneID"], "ENSG00000135916.15"),
        ([-1, "left", "chromosome"], "chr2"),
        ([-1, "left", "position"], 230865145),
        ([-1, "left", "strand"], "+"),
        ([-1, "right", "geneName"], "PTMA"),
        ([-1, "right", "geneID"], "ENSG00000187514.14"),
        ([-1, "right", "chromosome"], "chr2"),
        ([-1, "right", "position"], 231711348),
        ([-1, "right", "strand"], "+"),
    ],
)
def test_star_fusion_v060_01(star_fusion_v060_01, attrs, exp):
    assert getattr_nested(star_fusion_v060_01.json, attrs) == exp, ", ".join(
        [repr(x) for x in attrs]
    )


@pytest.mark.parametrize(
    "attrs, exp",
    [
        ([0, "fusionName"], "KANSL1--ARL17B"),
        ([0, "nJunctionReads"], 23),
        ([0, "nSpanningFrags"], 4),
        ([0, "spliceType"], "ONLY_REF_SPLICE"),
        ([0, "left", "geneName"], "KANSL1"),
        ([0, "left", "geneID"], "ENSG00000120071.12"),
        ([0, "left", "chromosome"], "chr17"),
        ([0, "left", "position"], 46094560),
        ([0, "left", "strand"], "-"),
        ([0, "right", "geneName"], "ARL17B"),
        ([0, "right", "geneID"], "ENSG00000228696.8"),
        ([0, "right", "chromosome"], "chr17"),
        ([0, "right", "position"], 46352930),
        ([0, "right", "strand"], "-"),
        ([0, "reads", "junctionReads", 0], "HISEQ:113:C6ALHANXX:5:1308:16235:84862"),
        ([0, "reads", "junctionReads", -1], "HISEQ:114:C6DWCANXX:4:2102:20538:80656"),
        ([0, "reads", "spanningFrags", 0], "HISEQ:114:C6DWCANXX:4:1102:11126:100433"),
        ([0, "reads", "spanningFrags", -1], "HISEQ:114:C6DWCANXX:4:1106:20997:30657"),
        ([-1, "fusionName"], "NCOR2--UBC"),
        ([-1, "nJunctionReads"], 1),
        ([-1, "nSpanningFrags"], 1),
        ([-1, "spliceType"], "ONLY_REF_SPLICE"),
        ([-1, "left", "geneName"], "NCOR2"),
        ([-1, "left", "geneID"], "ENSG00000196498.13"),
        ([-1, "left", "chromosome"], "chr12"),
        ([-1, "left", "position"], 124362126),
        ([-1, "left", "strand"], "-"),
        ([-1, "right", "geneName"], "UBC"),
        ([-1, "right", "geneID"], "ENSG00000150991.14"),
        ([-1, "right", "chromosome"], "chr12"),
        ([-1, "right", "position"], 124913774),
        ([-1, "right", "strand"], "-"),
        ([-1, "reads", "junctionReads", 0], "HISEQ:113:C6ALHANXX:5:1310:3755:40412"),
        ([-1, "reads", "junctionReads", -1], "HISEQ:113:C6ALHANXX:5:1310:3755:40412"),
        ([-1, "reads", "spanningFrags", 0], "HISEQ:114:C6DWCANXX:4:2101:4289:41779"),
        ([-1, "reads", "spanningFrags", -1], "HISEQ:114:C6DWCANXX:4:2101:4289:41779"),
    ],
)
def test_star_fusion_v060_02(star_fusion_v060_02, attrs, exp):
    assert getattr_nested(star_fusion_v060_02.json, attrs) == exp, ", ".join(
        [repr(x) for x in attrs]
    )


def test_star_fusion_v160_dummy_types(star_fusion_v160_dummy):
    """Test whether if the data fields have the correct type"""
    for result in star_fusion_v160_dummy.json:
        # Test int
        for field in ("nJunctionReads", "nSpanningFrags"):
            assert isinstance(result[field], int)

        # Test float
        assert isinstance(result["FFPM"], float)
        assert isinstance(result["left"]["breakEntropy"], float)
        assert isinstance(result["right"]["breakEntropy"], float)

        # Test list
        assert isinstance(result["annots"], list)
        assert isinstance(result["reads"]["junctionReads"], list)
        assert isinstance(result["reads"]["spanningFrags"], list)


def test_star_fusion_v160_abr_no_reads(star_fusion_v160_abr_dummy):
    """Test whether reads are absent from abridged output"""
    for result in star_fusion_v160_abr_dummy.json:
        assert "reads" not in result


def test_star_fusion_v160_empty_list(star_fusion_v160_dummy):
    second_result = star_fusion_v160_dummy.json[1]
    third_result = star_fusion_v160_dummy.json[2]

    assert second_result["reads"]["spanningFrags"] == []
    assert second_result["reads"]["junctionReads"] == ["read1", "read2"]
    assert third_result["reads"]["spanningFrags"] == []
    assert third_result["reads"]["junctionReads"] == []


@pytest.mark.parametrize(
    "attrs, exp",
    [
        ([0, "fusionName"], "PLAA--MIR31HG"),
        ([0, "nJunctionReads"], 200),
        ([0, "nSpanningFrags"], 101),
        ([0, "spliceType"], "ONLY_REF_SPLICE"),
        ([0, "FFPM"], 3.671),
        ([0, "largeAnchorSupport"], "YES_LDAS"),
        ([0, "annots", 0], "CCLE_StarF2019"),
        ([0, "annots", -1], "INTRACHROMOSOMAL[chr9:5.34Mb]"),
        ([0, "left", "geneName"], "PLAA"),
        ([0, "left", "geneID"], "ENSG00000137055.15"),
        ([0, "left", "chromosome"], "chr9"),
        ([0, "left", "position"], 26919310),
        ([0, "left", "strand"], "-"),
        ([0, "left", "breakDinuc"], "GT"),
        ([0, "left", "breakEntropy"], 1.9329),
        ([0, "right", "geneName"], "MIR31HG"),
        ([0, "right", "geneID"], "ENSG00000171889.4"),
        ([0, "right", "chromosome"], "chr9"),
        ([0, "right", "position"], 21455944),
        ([0, "right", "strand"], "-"),
        ([0, "right", "breakDinuc"], "AG"),
        ([0, "right", "breakEntropy"], 1.9329),
        ([0, "reads", "junctionReads", 0], "SRR8615343.84218969"),
        ([0, "reads", "junctionReads", -1], "SRR8615343.30282436"),
        ([0, "reads", "spanningFrags", 0], "SRR8615343.30281602"),
        ([0, "reads", "spanningFrags", -1], "SRR8615343.30278507"),
        ([-1, "fusionName"], "STX8--IDI2"),
        ([-1, "nJunctionReads"], 2),
        ([-1, "nSpanningFrags"], 8),
        ([-1, "spliceType"], "ONLY_REF_SPLICE"),
        ([-1, "FFPM"], 0.122),
        ([-1, "largeAnchorSupport"], "YES_LDAS"),
        ([-1, "annots", 0], "CCLE_StarF2019"),
        ([-1, "annots", -1], "INTERCHROMOSOMAL[chr17--chr10]"),
        ([-1, "left", "geneName"], "STX8"),
        ([-1, "left", "geneID"], "ENSG00000170310.15"),
        ([-1, "left", "chromosome"], "chr17"),
        ([-1, "left", "position"], 9545172),
        ([-1, "left", "strand"], "-"),
        ([-1, "left", "breakDinuc"], "GT"),
        ([-1, "left", "breakEntropy"], 1.8892),
        ([-1, "right", "geneName"], "IDI2"),
        ([-1, "right", "geneID"], "ENSG00000148377.6"),
        ([-1, "right", "chromosome"], "chr10"),
        ([-1, "right", "position"], 1022775),
        ([-1, "right", "strand"], "-"),
        ([-1, "right", "breakDinuc"], "AG"),
        ([-1, "right", "breakEntropy"], 1.8323),
        ([-1, "reads", "junctionReads", 0], "SRR8615343.54793320"),
        ([-1, "reads", "junctionReads", -1], "SRR8615343.97918844"),
        ([-1, "reads", "spanningFrags", 0], "SRR8615343.32910761"),
        ([-1, "reads", "spanningFrags", -1], "SRR8615343.93902364"),
    ],
)
def test_star_fusion_v160_NB4(star_fusion_v160_NB4, attrs, exp):
    assert getattr_nested(star_fusion_v160_NB4.json, attrs) == exp, ", ".join(
        [repr(x) for x in attrs]
    )


@pytest.mark.parametrize(
    "attrs, exp",
    [
        ([0, "fusionName"], "PLAA--MIR31HG"),
        ([0, "nJunctionReads"], 200),
        ([0, "nSpanningFrags"], 101),
        ([0, "spliceType"], "ONLY_REF_SPLICE"),
        ([0, "FFPM"], 3.671),
        ([0, "largeAnchorSupport"], "YES_LDAS"),
        ([0, "annots", 0], "CCLE_StarF2019"),
        ([0, "annots", -1], "INTRACHROMOSOMAL[chr9:5.34Mb]"),
        ([0, "left", "geneName"], "PLAA"),
        ([0, "left", "geneID"], "ENSG00000137055.15"),
        ([0, "left", "chromosome"], "chr9"),
        ([0, "left", "position"], 26919310),
        ([0, "left", "strand"], "-"),
        ([0, "left", "breakDinuc"], "GT"),
        ([0, "left", "breakEntropy"], 1.9329),
        ([0, "right", "geneName"], "MIR31HG"),
        ([0, "right", "geneID"], "ENSG00000171889.4"),
        ([0, "right", "chromosome"], "chr9"),
        ([0, "right", "position"], 21455944),
        ([0, "right", "strand"], "-"),
        ([0, "right", "breakDinuc"], "AG"),
        ([0, "right", "breakEntropy"], 1.9329),
        ([-1, "fusionName"], "STX8--IDI2"),
        ([-1, "nJunctionReads"], 2),
        ([-1, "nSpanningFrags"], 8),
        ([-1, "spliceType"], "ONLY_REF_SPLICE"),
        ([-1, "FFPM"], 0.122),
        ([-1, "largeAnchorSupport"], "YES_LDAS"),
        ([-1, "annots", 0], "CCLE_StarF2019"),
        ([-1, "annots", -1], "INTERCHROMOSOMAL[chr17--chr10]"),
        ([-1, "left", "geneName"], "STX8"),
        ([-1, "left", "geneID"], "ENSG00000170310.15"),
        ([-1, "left", "chromosome"], "chr17"),
        ([-1, "left", "position"], 9545172),
        ([-1, "left", "strand"], "-"),
        ([-1, "left", "breakDinuc"], "GT"),
        ([-1, "left", "breakEntropy"], 1.8892),
        ([-1, "right", "geneName"], "IDI2"),
        ([-1, "right", "geneID"], "ENSG00000148377.6"),
        ([-1, "right", "chromosome"], "chr10"),
        ([-1, "right", "position"], 1022775),
        ([-1, "right", "strand"], "-"),
        ([-1, "right", "breakDinuc"], "AG"),
        ([-1, "right", "breakEntropy"], 1.8323),
    ],
)
def test_star_fusion_v160_abr_NB4(star_fusion_v160_abr_NB4, attrs, exp):
    assert getattr_nested(star_fusion_v160_abr_NB4.json, attrs) == exp, ", ".join(
        [repr(x) for x in attrs]
    )


def test_parse_rl_entry_raises():
    with pytest.raises(RuntimeError):
        parse_lr_entry("middle", dict())


def test_parse_raw_line_raises():
    with pytest.raises(BadParameter):
        parse_raw_line(raw_line="Wrong raw line", version="v1.6.0")


def test_detect_format_raises():
    with pytest.raises(BadParameter):
        detect_format(colnames="Wrong column names")


def test_parse_annots_raises():
    with pytest.raises(RuntimeError):
        parse_annots("Does not start with [")
