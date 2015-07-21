# -*- coding: utf-8 -*-
"""
    crimson.tests.test_flagstat
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Flagstat subcommand tests.

    :copyright: (c) 2015 Wibowo Arindrarto <bow@bow.web.id>
    :license: BSD

"""
import json
import pytest
from click.testing import CliRunner

from crimson.main import cli

from .utils import get_test_file


@pytest.fixture(scope="module")
def flagstat_v0119_01():
    runner = CliRunner()
    in_file = get_test_file("samtools_flagstat_v0119_01.txt")
    result = runner.invoke(cli, ["flagstat", in_file, "-"])
    result.json = json.loads(result.output)
    return result


@pytest.fixture(scope="module")
def flagstat_v11_01():
    runner = CliRunner()
    in_file = get_test_file("samtools_flagstat_v11_01.txt")
    result = runner.invoke(cli, ["flagstat", in_file, "-"])
    result.json = json.loads(result.output)
    return result


def test_flagstat_v0119_01_exit_code(flagstat_v0119_01):
    assert flagstat_v0119_01.exit_code == 0


@pytest.mark.parametrize("attr, exp", [
    ("total", 14152593),
    ("duplicates", 0),
    ("mapped", 13391622),
    ("paired_sequencing", 14152593),
    ("paired", 13356881),
    ("paired_proper", 13331891),
    ("read1", 7076309),
    ("read2", 7076284),
    ("singleton", 34741),
    ("diff_chrom", 26959),
    ("diff_chrom_mapq", 26959),
])
def test_flagstat_v0119_01_pass_qc(flagstat_v0119_01, attr, exp):
    assert flagstat_v0119_01.json.get("pass_qc", {}).get(attr) == exp


@pytest.mark.parametrize("attr, exp", [
    ("total", 0),
    ("duplicates", 0),
    ("mapped", 0),
    ("paired_sequencing", 0),
    ("paired", 0),
    ("paired_proper", 0),
    ("read1", 0),
    ("read2", 0),
    ("singleton", 0),
    ("diff_chrom", 0),
    ("diff_chrom_mapq", 0),
])
def test_flagstat_v0119_01_fail_qc(flagstat_v0119_01, attr, exp):
    assert flagstat_v0119_01.json.get("fail_qc", {}).get(attr) == exp


def test_flagstat_v11_01_exit_code(flagstat_v11_01):
    assert flagstat_v11_01.exit_code == 0


@pytest.mark.parametrize("attr, exp", [
    ("total", 71511),
    ("secondary", 122),
    ("supplimentary", 0),
    ("duplicates", 0),
    ("mapped", 71228),
    ("paired_sequencing", 71389),
    ("paired", 71070),
    ("paired_proper", 70374),
    ("read1", 35691),
    ("read2", 35698),
    ("singleton", 36),
    ("diff_chrom", 446),
    ("diff_chrom_mapq", 192),
])
def test_flagstat_v11_01_pass_qc(flagstat_v11_01, attr, exp):
    assert flagstat_v11_01.json.get("pass_qc", {}).get(attr) == exp


@pytest.mark.parametrize("attr, exp", [
    ("total", 0),
    ("secondary", 0),
    ("supplimentary", 0),
    ("duplicates", 0),
    ("mapped", 0),
    ("paired_sequencing", 0),
    ("paired", 0),
    ("paired_proper", 0),
    ("read1", 0),
    ("read2", 0),
    ("singleton", 0),
    ("diff_chrom", 0),
    ("diff_chrom_mapq", 0),
])
def test_flagstat_v11_01_fail_qc(flagstat_v11_01, attr, exp):
    assert flagstat_v11_01.json.get("fail_qc", {}).get(attr) == exp
