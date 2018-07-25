# -*- coding: utf-8 -*-
"""
    star-fusion subcommand tests
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
# (c) 2015-2018 Wibowo Arindrarto <bow@bow.web.id>
import json
import pytest
from click.testing import CliRunner

from crimson.cli import main

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


def test_star_fusion_fail_exit_code(star_fusion_fail):
    assert star_fusion_fail.exit_code != 0


def test_star_fusion_fail_output(star_fusion_fail):
    err_msg = "Unexpected header line:"
    assert err_msg in star_fusion_fail.output


@pytest.mark.parametrize("attrs, exp", [
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
])
def test_star_fusion_v060_01(star_fusion_v060_01, attrs, exp):
    assert getattr_nested(star_fusion_v060_01.json, attrs) == exp, \
        ", ".join([repr(x) for x in attrs])


@pytest.mark.parametrize("attrs, exp", [
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
    ([0, "reads", "junctionReads", 0],
     "HISEQ:113:C6ALHANXX:5:1308:16235:84862"),
    ([0, "reads", "junctionReads", -1],
     "HISEQ:114:C6DWCANXX:4:2102:20538:80656"),
    ([0, "reads", "spanningFrags", 0],
     "HISEQ:114:C6DWCANXX:4:1102:11126:100433"),
    ([0, "reads", "spanningFrags", -1],
     "HISEQ:114:C6DWCANXX:4:1106:20997:30657"),
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
    ([-1, "reads", "junctionReads", 0],
     "HISEQ:113:C6ALHANXX:5:1310:3755:40412"),
    ([-1, "reads", "junctionReads", -1],
     "HISEQ:113:C6ALHANXX:5:1310:3755:40412"),
    ([-1, "reads", "spanningFrags", 0],
     "HISEQ:114:C6DWCANXX:4:2101:4289:41779"),
    ([-1, "reads", "spanningFrags", -1],
     "HISEQ:114:C6DWCANXX:4:2101:4289:41779"),
])
def test_star_fusion_v060_02(star_fusion_v060_02, attrs, exp):
    assert getattr_nested(star_fusion_v060_02.json, attrs) == exp, \
        ", ".join([repr(x) for x in attrs])
