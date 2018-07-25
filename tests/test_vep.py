# -*- coding: utf-8 -*-
"""
    vep subcommand tests
    ~~~~~~~~~~~~~~~~~~~~

"""
# (c) 2015-2018 Wibowo Arindrarto <bow@bow.web.id>
import json
import pytest
from click.testing import CliRunner

from crimson.cli import main

from .utils import getattr_nested, get_test_path


@pytest.fixture(scope="module")
def vep_fail():
    runner = CliRunner()
    in_file = get_test_path("vep_nope.txt")
    result = runner.invoke(main, ["vep", in_file])
    return result


@pytest.fixture(scope="module")
def vep_v77_01():
    runner = CliRunner()
    in_file = get_test_path("vep_v77_01.txt")
    result = runner.invoke(main, ["vep", in_file])
    result.json = json.loads(result.output)
    return result


def test_vep_fail_exit_code(vep_fail):
    assert vep_fail.exit_code != 0


def test_vep_fail_output(vep_fail):
    err_msg = "Unexpected file structure. No contents parsed."
    assert err_msg in vep_fail.output


@pytest.mark.parametrize("attrs, exp", [
    (["VEP run statistics", "Cache/Database"],
     "/home/user/.vep/homo_sapiens/77_GRCh38"),
    (["Variant classes", "insertion"], 35),
    (["Variant classes", "deletion"], 18),
    (["Variant classes", "SNV"], 448),
    (["Variants by chromosome", "1"], 42),
    (["Variants by chromosome", "21"], 45),
    (["Position in protein", "90-100%"], 7),
    (["Distribution of variants on chromosome 21", 46], 0),
])
def test_vep_v77_01(vep_v77_01, attrs, exp):
    assert getattr_nested(vep_v77_01.json, attrs) == exp, \
        ", ".join([repr(x) for x in attrs])
