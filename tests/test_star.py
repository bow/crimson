# -*- coding: utf-8 -*-
"""
    star subcommand tests
    ~~~~~~~~~~~~~~~~~~~~~

"""
# (c) 2015-2018 Wibowo Arindrarto <bow@bow.web.id>
import json
import pytest
from click.testing import CliRunner

from crimson.cli import main

from .utils import get_test_path


@pytest.fixture(scope="module")
def star_fail():
    runner = CliRunner()
    in_file = get_test_path("star_nope.txt")
    result = runner.invoke(main, ["star", in_file])
    return result


@pytest.fixture(scope="module")
def star_v230_01():
    runner = CliRunner()
    in_file = get_test_path("star_v230_01.txt")
    result = runner.invoke(main, ["star", in_file])
    result.json = json.loads(result.output)
    return result


@pytest.fixture(scope="module")
def star_v230_02():
    runner = CliRunner()
    in_file = get_test_path("star_v230_02.txt")
    result = runner.invoke(main, ["star", in_file])
    result.json = json.loads(result.output)
    return result


def test_star_fail_exit_code(star_fail):
    assert star_fail.exit_code != 0


def test_star_fail_output(star_fail):
    err_msg = "Unexpected file structure. No contents parsed."
    assert err_msg in star_fail.output


@pytest.mark.parametrize("attr, exp", [
    ("avgDeletionLength", 1.36),
    ("avgInputLength", 98),
    ("avgInsertionLength", 1.21),
    ("avgMappedLength", 98.27),
    ("mappingSpeed", 403.16),
    ("nInput", 14782416),
    ("nMappedMultipleLoci", 1936775),
    ("nMappedTooManyLoci", 27644),
    ("nSplicesATAC", 2471),
    ("nSplicesAnnotated", 3780876),
    ("nSplicesGCAG", 22344),
    ("nSplicesGTAG", 3780050),
    ("nSplicesNonCanonical", 5148),
    ("nSplicesTotal", 3810013),
    ("nUniquelyMapped", 12347431),
    ("pctMappedMultipleLoci", 13.1),
    ("pctMappedTooManyLoci", 0.19),
    ("pctUniquelyMapped", 83.53),
    ("pctUnmappedForOther", 0.03),
    ("pctUnmappedForTooManyMismatches", 0.0),
    ("pctUnmappedForTooShort", 3.16),
    ("rateDeletionPerBase", 0.0),
    ("rateInsertionPerBase", 0.0),
    ("rateMismatchPerBase", 0.24),
    ("timeEnd", "Dec 11 19:01:56"),
    ("timeJobStart", "Dec 11 18:55:02"),
    ("timeMappingStart", "Dec 11 18:59:44"),
])
def test_star_v230_01(star_v230_01, attr, exp):
    assert star_v230_01.json.get(attr) == exp, attr
