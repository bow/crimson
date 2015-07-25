# -*- coding: utf-8 -*-
"""
    crimson.tests.test_picard
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    Picard subcommand tests.

    :copyright: (c) 2015 Wibowo Arindrarto <bow@bow.web.id>
    :license: BSD

"""
import json
import pytest
from click.testing import CliRunner

from crimson.main import cli

from .utils import get_test_file, getattr_nested


@pytest.fixture(scope="module")
def picard_fail():
    runner = CliRunner()
    in_file = get_test_file("picard_nope.txt")
    result = runner.invoke(cli, ["picard", in_file, "-"])
    return result


def test_picard_fail_exit_code(picard_fail):
    assert picard_fail.exit_code != 0


@pytest.fixture(scope="module")
def alignment_summary_v1124_01():
    runner = CliRunner()
    in_file = get_test_file("picard_alignment_summary_v1124_01.txt")
    result = runner.invoke(cli, ["picard", in_file, "-"])
    result.json = json.loads(result.output)
    return result


def test_alignment_summary_v1124_01_exit_code(alignment_summary_v1124_01):
    assert alignment_summary_v1124_01.exit_code == 0


@pytest.mark.parametrize("attrs, exp", [
    (["header", "time"], "Started on: Sun Jul 19 15:42:28 CEST 2015"),
    (["metrics", "class"], "picard.analysis.AlignmentSummaryMetrics"),
    (["metrics", "contents", 0, "CATEGORY"], "FIRST_OF_PAIR"),
    (["metrics", "contents", 0, "TOTAL_READS"], 35691),
    (["metrics", "contents", 0, "PF_READS"], 35691),
    (["metrics", "contents", 0, "PCT_PF_READS"], 1),
    (["metrics", "contents", 0, "PF_NOISE_READS"], 0),
    (["metrics", "contents", 0, "PF_READS_ALIGNED"], 35557),
    (["metrics", "contents", 0, "PCT_PF_READS_ALIGNED"], 0.996246),
    (["metrics", "contents", 0, "PF_ALIGNED_BASES"], 3501223),
    (["metrics", "contents", 0, "PF_HQ_ALIGNED_READS"], 33864),
    (["metrics", "contents", 0, "PF_HQ_ALIGNED_BASES"], 3346832),
    (["metrics", "contents", 0, "PF_HQ_ALIGNED_Q20_BASES"], 3334799),
    (["metrics", "contents", 0, "PF_HQ_MEDIAN_MISMATCHES"], 0),
    (["metrics", "contents", 0, "PF_MISMATCH_RATE"], 0.002714),
    (["metrics", "contents", 0, "PF_HQ_ERROR_RATE"], 0.001829),
    (["metrics", "contents", 0, "PF_INDEL_RATE"], 0.000208),
    (["metrics", "contents", 0, "MEAN_READ_LENGTH"], 99.003895),
    (["metrics", "contents", 0, "READS_ALIGNED_IN_PAIRS"], 35535),
    (["metrics", "contents", 0, "PCT_READS_ALIGNED_IN_PAIRS"], 0.999381),
    (["metrics", "contents", 0, "BAD_CYCLES"], 0),
    (["metrics", "contents", 0, "STRAND_BALANCE"], 0.500464),
    (["metrics", "contents", 0, "PCT_CHIMERAS"], 0.007275),
    (["metrics", "contents", 0, "PCT_ADAPTER"], 0.000224),
    (["metrics", "contents", 0, "SAMPLE"], ""),
    (["metrics", "contents", 0, "LIBRARY"], ""),
    (["metrics", "contents", 0, "READ_GROUP"], ""),
    (["metrics", "contents", 2, "CATEGORY"], "PAIR"),
    (["metrics", "contents", 2, "TOTAL_READS"], 71389),
    (["metrics", "contents", 2, "PF_READS"], 71389),
    (["metrics", "contents", 2, "PCT_PF_READS"], 1),
    (["metrics", "contents", 2, "PF_NOISE_READS"], 0),
    (["metrics", "contents", 2, "PF_READS_ALIGNED"], 71106),
    (["metrics", "contents", 2, "PCT_PF_READS_ALIGNED"], 0.996036),
    (["metrics", "contents", 2, "PF_ALIGNED_BASES"], 6945691),
    (["metrics", "contents", 2, "PF_HQ_ALIGNED_READS"], 67701),
    (["metrics", "contents", 2, "PF_HQ_ALIGNED_BASES"], 6638298),
    (["metrics", "contents", 2, "PF_HQ_ALIGNED_Q20_BASES"], 6607469),
    (["metrics", "contents", 2, "PF_HQ_MEDIAN_MISMATCHES"], 0),
    (["metrics", "contents", 2, "PF_MISMATCH_RATE"], 0.002845),
    (["metrics", "contents", 2, "PF_HQ_ERROR_RATE"], 0.001944),
    (["metrics", "contents", 2, "PF_INDEL_RATE"], 0.000197),
    (["metrics", "contents", 2, "MEAN_READ_LENGTH"], 98.213983),
    (["metrics", "contents", 2, "READS_ALIGNED_IN_PAIRS"], 71070),
    (["metrics", "contents", 2, "PCT_READS_ALIGNED_IN_PAIRS"], 0.999494),
    (["metrics", "contents", 2, "BAD_CYCLES"], 0),
    (["metrics", "contents", 2, "STRAND_BALANCE"], 0.500127),
    (["metrics", "contents", 2, "PCT_CHIMERAS"], 0.007275),
    (["metrics", "contents", 2, "PCT_ADAPTER"], 0.000224),
    (["metrics", "contents", 2, "SAMPLE"], ""),
    (["metrics", "contents", 2, "LIBRARY"], ""),
    (["metrics", "contents", 2, "READ_GROUP"], ""),
    (["metrics", "contents", 3], None),
    (["histogram"], None),
])
def test_alignment_summary_v1124_01(alignment_summary_v1124_01, attrs, exp):
    assert getattr_nested(alignment_summary_v1124_01.json, attrs) == exp, \
        ", ".join([repr(x) for x in attrs])
