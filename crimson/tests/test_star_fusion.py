# -*- coding: utf-8 -*-
"""
    crimson.tests.test_star_fusion
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    star-fusion subcommand tests.

    :copyright: (c) 2016 Wibowo Arindrarto <bow@bow.web.id>
    :license: BSD

"""
import json
import pytest
from click.testing import CliRunner

from crimson.main import cli

from .utils import get_test_path, getattr_nested


@pytest.fixture(scope="module")
def star_fusion_fail():
    runner = CliRunner()
    in_file = get_test_path("star_fusion_nope.txt")
    result = runner.invoke(cli, ["star-fusion", in_file])
    return result


@pytest.fixture(scope="module")
def star_fusion_v060_01():
    runner = CliRunner()
    in_file = get_test_path("star_fusion_v060_01.txt")
    result = runner.invoke(cli, ["star-fusion", in_file])
    result.json = json.loads(result.output)
    return result


def test_star_fusion_fail_exit_code(star_fusion_fail):
    assert star_fusion_fail.exit_code != 0


def test_star_fusion_fail_output(star_fusion_fail):
    err_msg = "Unexpected header line:"
    assert err_msg in star_fusion_fail.output


@pytest.mark.parametrize("attrs, exp", [
    ([0, "name"], "RUNX1--RUNX1T1"),
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
    ([-1, "name"], "ITM2C--PTMA"),
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
def test_star_fusion_v060_01_pass_qc(star_fusion_v060_01, attrs, exp):
    assert getattr_nested(star_fusion_v060_01.json, attrs) == exp, \
        ", ".join([repr(x) for x in attrs])
