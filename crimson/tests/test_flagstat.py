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

def test_flagstat_v0119_01_exit_code(flagstat_v0119_01):
    assert flagstat_v0119_01.exit_code == 0

def test_flagstat_v0119_01_pass_qc_total(flagstat_v0119_01):
    assert flagstat_v0119_01.json["pass_qc"]["total"] == 14152593
    assert flagstat_v0119_01.json["fail_qc"]["total"] == 0

def test_flagstat_v0119_01_pass_qc_mapped(flagstat_v0119_01):
    assert flagstat_v0119_01.json["pass_qc"]["mapped"] == 13391622
    assert flagstat_v0119_01.json["fail_qc"]["mapped"] == 0

def test_flagstat_v0119_01_pass_qc_paired_sequencing(flagstat_v0119_01):
    assert flagstat_v0119_01.json["pass_qc"]["paired_sequencing"] == 14152593
    assert flagstat_v0119_01.json["fail_qc"]["paired_sequencing"] == 0

def test_flagstat_v0119_01_pass_qc_paired(flagstat_v0119_01):
    assert flagstat_v0119_01.json["pass_qc"]["paired"] == 13356881
    assert flagstat_v0119_01.json["fail_qc"]["paired"] == 0

def test_flagstat_v0119_01_pass_qc_paired_proper(flagstat_v0119_01):
    assert flagstat_v0119_01.json["pass_qc"]["paired_proper"] == 13331891
    assert flagstat_v0119_01.json["fail_qc"]["paired_proper"] == 0

def test_flagstat_v0119_01_pass_qc_read1(flagstat_v0119_01):
    assert flagstat_v0119_01.json["pass_qc"]["read1"] == 7076309
    assert flagstat_v0119_01.json["fail_qc"]["read1"] == 0

def test_flagstat_v0119_01_pass_qc_read2(flagstat_v0119_01):
    assert flagstat_v0119_01.json["pass_qc"]["read2"] == 7076284
    assert flagstat_v0119_01.json["fail_qc"]["read2"] == 0

def test_flagstat_v0119_01_pass_qc_singleton(flagstat_v0119_01):
    assert flagstat_v0119_01.json["pass_qc"]["singleton"] == 34741
    assert flagstat_v0119_01.json["fail_qc"]["singleton"] == 0

def test_flagstat_v0119_01_pass_qc_diff_chrom(flagstat_v0119_01):
    assert flagstat_v0119_01.json["pass_qc"]["diff_chrom"] == 26959
    assert flagstat_v0119_01.json["fail_qc"]["diff_chrom"] == 0

def test_flagstat_v0119_01_pass_qc_diff_chrom_mapq(flagstat_v0119_01):
    assert flagstat_v0119_01.json["pass_qc"]["diff_chrom_mapq"] == 26959
    assert flagstat_v0119_01.json["fail_qc"]["diff_chrom_mapq"] == 0
