# -*- coding: utf-8 -*-
"""
    picard subcommand tests
    ~~~~~~~~~~~~~~~~~~~~~~~

"""
# (c) 2015-2018 Wibowo Arindrarto <bow@bow.web.id>
import json
import pytest
from click.testing import CliRunner

from crimson.cli import main

from .utils import get_test_path, getattr_nested


@pytest.fixture(scope="module")
def picard_fail():
    runner = CliRunner()
    in_file = get_test_path("picard_nope.txt")
    result = runner.invoke(main, ["picard", in_file])
    return result


def test_picard_fail_exit_code(picard_fail):
    assert picard_fail.exit_code != 0


@pytest.fixture(scope="module")
def alignment_summary_v1124_01():
    runner = CliRunner()
    in_file = get_test_path("picard_alignment_summary_v1124_01.txt")
    result = runner.invoke(main, ["picard", in_file])
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
    (["metrics", "contents", -1, "CATEGORY"], "PAIR"),
    (["metrics", "contents", -1, "TOTAL_READS"], 71389),
    (["metrics", "contents", -1, "PF_READS"], 71389),
    (["metrics", "contents", -1, "PCT_PF_READS"], 1),
    (["metrics", "contents", -1, "PF_NOISE_READS"], 0),
    (["metrics", "contents", -1, "PF_READS_ALIGNED"], 71106),
    (["metrics", "contents", -1, "PCT_PF_READS_ALIGNED"], 0.996036),
    (["metrics", "contents", -1, "PF_ALIGNED_BASES"], 6945691),
    (["metrics", "contents", -1, "PF_HQ_ALIGNED_READS"], 67701),
    (["metrics", "contents", -1, "PF_HQ_ALIGNED_BASES"], 6638298),
    (["metrics", "contents", -1, "PF_HQ_ALIGNED_Q20_BASES"], 6607469),
    (["metrics", "contents", -1, "PF_HQ_MEDIAN_MISMATCHES"], 0),
    (["metrics", "contents", -1, "PF_MISMATCH_RATE"], 0.002845),
    (["metrics", "contents", -1, "PF_HQ_ERROR_RATE"], 0.001944),
    (["metrics", "contents", -1, "PF_INDEL_RATE"], 0.000197),
    (["metrics", "contents", -1, "MEAN_READ_LENGTH"], 98.213983),
    (["metrics", "contents", -1, "READS_ALIGNED_IN_PAIRS"], 71070),
    (["metrics", "contents", -1, "PCT_READS_ALIGNED_IN_PAIRS"], 0.999494),
    (["metrics", "contents", -1, "BAD_CYCLES"], 0),
    (["metrics", "contents", -1, "STRAND_BALANCE"], 0.500127),
    (["metrics", "contents", -1, "PCT_CHIMERAS"], 0.007275),
    (["metrics", "contents", -1, "PCT_ADAPTER"], 0.000224),
    (["metrics", "contents", -1, "SAMPLE"], ""),
    (["metrics", "contents", -1, "LIBRARY"], ""),
    (["metrics", "contents", -1, "READ_GROUP"], ""),
    (["histogram"], None),
])
def test_alignment_summary_v1124_01(alignment_summary_v1124_01, attrs, exp):
    assert getattr_nested(alignment_summary_v1124_01.json, attrs) == exp, \
        ", ".join([repr(x) for x in attrs])


@pytest.fixture(scope="module")
def insert_size_v1124_01():
    runner = CliRunner()
    in_file = get_test_path("picard_insert_size_v1124_01.txt")
    result = runner.invoke(main, ["picard", in_file])
    result.json = json.loads(result.output)
    return result


def test_insert_size_v1124_01_exit_code(insert_size_v1124_01):
    assert insert_size_v1124_01.exit_code == 0


@pytest.mark.parametrize("attrs, exp", [
    (["header", "time"], "Started on: Sun Jul 19 15:42:28 CEST 2015"),
    (["metrics", "class"], "picard.analysis.InsertSizeMetrics"),
    (["metrics", "contents", "MEDIAN_INSERT_SIZE"], 317),
    (["metrics", "contents", "MEDIAN_ABSOLUTE_DEVIATION"], 44),
    (["metrics", "contents", "MIN_INSERT_SIZE"], 13),
    (["metrics", "contents", "MAX_INSERT_SIZE"], 23587641),
    (["metrics", "contents", "MEAN_INSERT_SIZE"], 316.523985),
    (["metrics", "contents", "STANDARD_DEVIATION"], 74.454708),
    (["metrics", "contents", "READ_PAIRS"], 35243),
    (["metrics", "contents", "PAIR_ORIENTATION"], "FR"),
    (["metrics", "contents", "WIDTH_OF_10_PERCENT"], 17),
    (["metrics", "contents", "WIDTH_OF_20_PERCENT"], 33),
    (["metrics", "contents", "WIDTH_OF_30_PERCENT"], 51),
    (["metrics", "contents", "WIDTH_OF_40_PERCENT"], 69),
    (["metrics", "contents", "WIDTH_OF_50_PERCENT"], 89),
    (["metrics", "contents", "WIDTH_OF_60_PERCENT"], 113),
    (["metrics", "contents", "WIDTH_OF_70_PERCENT"], 141),
    (["metrics", "contents", "WIDTH_OF_80_PERCENT"], 179),
    (["metrics", "contents", "WIDTH_OF_90_PERCENT"], 245),
    (["metrics", "contents", "WIDTH_OF_99_PERCENT"], 449),
    (["metrics", "contents", "SAMPLE"], ""),
    (["metrics", "contents", "LIBRARY"], ""),
    (["metrics", "contents", "READ_GROUP"], ""),
    (["histogram", "contents", 0, "insert_size"], 13),
    (["histogram", "contents", 0, "All_Reads.fr_count"], 1),
    (["histogram", "contents", -1, "insert_size"], 739),
    (["histogram", "contents", -1, "All_Reads.fr_count"], 1),
])
def test_insert_size_v1124_01(insert_size_v1124_01, attrs, exp):
    assert getattr_nested(insert_size_v1124_01.json, attrs) == exp, \
        ", ".join([repr(x) for x in attrs])


@pytest.fixture(scope="module")
def library_complexity_v1124_01():
    runner = CliRunner()
    in_file = get_test_path("picard_library_complexity_v1124_01.txt")
    result = runner.invoke(main, ["picard", in_file])
    result.json = json.loads(result.output)
    return result


def test_library_complexity_v1124_01_exit_code(library_complexity_v1124_01):
    assert library_complexity_v1124_01.exit_code == 0


@pytest.mark.parametrize("attrs, exp", [
    (["header", "time"], "Started on: Sun Jul 19 15:42:28 CEST 2015"),
    (["metrics", "class"], "picard.sam.DuplicationMetrics"),
    (["metrics", "contents", "LIBRARY"], "Unknown"),
    (["metrics", "contents", "UNPAIRED_READS_EXAMINED"], 0),
    (["metrics", "contents", "READ_PAIRS_EXAMINED"], 35637),
    (["metrics", "contents", "UNMAPPED_READS"], 0),
    (["metrics", "contents", "UNPAIRED_READ_DUPLICATES"], 0),
    (["metrics", "contents", "READ_PAIR_DUPLICATES"], 0),
    (["metrics", "contents", "READ_PAIR_OPTICAL_DUPLICATES"], 0),
    (["metrics", "contents", "PERCENT_DUPLICATION"], 0),
    (["metrics", "contents", "ESTIMATED_LIBRARY_SIZE"], ""),
    (["histogram", "contents", 0, "duplication_group_count"], 1),
    (["histogram", "contents", 0, "Unknown"], 35637),
    (["histogram", "contents", -1, "duplication_group_count"], 7),
    (["histogram", "contents", -1, "Unknown"], 1),
])
def test_library_complexity_v1124_01(library_complexity_v1124_01, attrs, exp):
    assert getattr_nested(library_complexity_v1124_01.json, attrs) == exp, \
        ", ".join([repr(x) for x in attrs])


@pytest.fixture(scope="module")
def mark_duplicates_v1124_01():
    runner = CliRunner()
    in_file = get_test_path("picard_mark_duplicates_v1124_01.txt")
    result = runner.invoke(main, ["picard", in_file])
    result.json = json.loads(result.output)
    return result


def test_mark_duplicates_v1124_01_exit_code(mark_duplicates_v1124_01):
    assert mark_duplicates_v1124_01.exit_code == 0


@pytest.mark.parametrize("attrs, exp", [
    (["header", "time"], "Started on: Sun Jul 19 15:42:34 CEST 2015"),
    (["metrics", "class"], "picard.sam.DuplicationMetrics"),
    (["metrics", "contents", "LIBRARY"], "SASC"),
    (["metrics", "contents", "UNPAIRED_READS_EXAMINED"], 36),
    (["metrics", "contents", "READ_PAIRS_EXAMINED"], 35535),
    (["metrics", "contents", "UNMAPPED_READS"], 283),
    (["metrics", "contents", "UNPAIRED_READ_DUPLICATES"], 0),
    (["metrics", "contents", "READ_PAIR_DUPLICATES"], 0),
    (["metrics", "contents", "READ_PAIR_OPTICAL_DUPLICATES"], 0),
    (["metrics", "contents", "PERCENT_DUPLICATION"], 0),
    (["metrics", "contents", "ESTIMATED_LIBRARY_SIZE"], ""),
    (["histogram"], None),
])
def test_mark_duplicates_v1124_01(mark_duplicates_v1124_01, attrs, exp):
    assert getattr_nested(mark_duplicates_v1124_01.json, attrs) == exp, \
        ", ".join([repr(x) for x in attrs])


@pytest.fixture(scope="module")
def rna_seq_v1124_01():
    runner = CliRunner()
    in_file = get_test_path("picard_rna_seq_v1124_01.txt")
    result = runner.invoke(main, ["picard", in_file])
    result.json = json.loads(result.output)
    return result


def test_rna_seq_v1124_01_exit_code(rna_seq_v1124_01):
    assert rna_seq_v1124_01.exit_code == 0


@pytest.mark.parametrize("attrs, exp", [
    (["header", "time"], "Started on: Sun Jul 19 15:42:28 CEST 2015"),
    (["metrics", "class"], "picard.analysis.RnaSeqMetrics"),
    (["metrics", "contents", "PF_BASES"], 32309274),
    (["metrics", "contents", "PF_ALIGNED_BASES"], 30461277),
    (["metrics", "contents", "RIBOSOMAL_BASES"], ""),
    (["metrics", "contents", "CODING_BASES"], 10026319),
    (["metrics", "contents", "UTR_BASES"], 8691712),
    (["metrics", "contents", "INTRONIC_BASES"], 3054788),
    (["metrics", "contents", "INTERGENIC_BASES"], 8688458),
    (["metrics", "contents", "IGNORED_READS"], 0),
    (["metrics", "contents", "CORRECT_STRAND_READS"], 0),
    (["metrics", "contents", "INCORRECT_STRAND_READS"], 0),
    (["metrics", "contents", "PCT_RIBOSOMAL_BASES"], ""),
    (["metrics", "contents", "PCT_CODING_BASES"], 0.32915),
    (["metrics", "contents", "PCT_UTR_BASES"], 0.285336),
    (["metrics", "contents", "PCT_INTRONIC_BASES"], 0.100284),
    (["metrics", "contents", "PCT_INTERGENIC_BASES"], 0.28523),
    (["metrics", "contents", "PCT_MRNA_BASES"], 0.614486),
    (["metrics", "contents", "PCT_USABLE_BASES"], 0.579339),
    (["metrics", "contents", "PCT_CORRECT_STRAND_READS"], 0),
    (["metrics", "contents", "MEDIAN_CV_COVERAGE"], 0.900974),
    (["metrics", "contents", "MEDIAN_5PRIME_BIAS"], 0.048295),
    (["metrics", "contents", "MEDIAN_3PRIME_BIAS"], 0.353777),
    (["metrics", "contents", "MEDIAN_5PRIME_TO_3PRIME_BIAS"], 0.415094),
    (["metrics", "contents", "SAMPLE"], ""),
    (["metrics", "contents", "LIBRARY"], ""),
    (["metrics", "contents", "READ_GROUP"], ""),
    (["histogram", "contents", 0, "normalized_position"], 0),
    (["histogram", "contents", 0, "All_Reads.normalized_coverage"], 0.039599),
    (["histogram", "contents", -1, "normalized_position"], 100),
    (["histogram", "contents", -1, "All_Reads.normalized_coverage"], 0.142949),
])
def test_rna_seq_v1124_01(rna_seq_v1124_01, attrs, exp):
    assert getattr_nested(rna_seq_v1124_01.json, attrs) == exp, \
        ", ".join([repr(x) for x in attrs])


@pytest.fixture(scope="module")
def wgs_v1124_01():
    runner = CliRunner()
    in_file = get_test_path("picard_wgs_v1124_01.txt")
    result = runner.invoke(main, ["picard", in_file])
    result.json = json.loads(result.output)
    return result


def test_wgs_v1124_01_exit_code(wgs_v1124_01):
    assert wgs_v1124_01.exit_code == 0


@pytest.mark.parametrize("attrs, exp", [
    (["header", "time"], "Started on: Sun Jul 19 15:42:28 CEST 2015"),
    (["metrics", "class"], "picard.analysis.CollectWgsMetrics$WgsMetrics"),
    (["metrics", "contents", "GENOME_TERRITORY"], 2867454345),
    (["metrics", "contents", "MEAN_COVERAGE"], 0.002278),
    (["metrics", "contents", "SD_COVERAGE"], 0.047962),
    (["metrics", "contents", "MEDIAN_COVERAGE"], 0),
    (["metrics", "contents", "MAD_COVERAGE"], 0),
    (["metrics", "contents", "PCT_EXC_MAPQ"], 0.044831),
    (["metrics", "contents", "PCT_EXC_DUPE"], 0),
    (["metrics", "contents", "PCT_EXC_UNPAIRED"], 0.000299),
    (["metrics", "contents", "PCT_EXC_BASEQ"], 0.004426),
    (["metrics", "contents", "PCT_EXC_OVERLAP"], 0.010468),
    (["metrics", "contents", "PCT_EXC_CAPPED"], 0),
    (["metrics", "contents", "PCT_EXC_TOTAL"], 0.060025),
    (["metrics", "contents", "PCT_5X"], 0),
    (["metrics", "contents", "PCT_10X"], 0),
    (["metrics", "contents", "PCT_15X"], 0),
    (["metrics", "contents", "PCT_20X"], 0),
    (["metrics", "contents", "PCT_25X"], 0),
    (["metrics", "contents", "PCT_30X"], 0),
    (["metrics", "contents", "PCT_40X"], 0),
    (["metrics", "contents", "PCT_50X"], 0),
    (["metrics", "contents", "PCT_60X"], 0),
    (["metrics", "contents", "PCT_70X"], 0),
    (["metrics", "contents", "PCT_80X"], 0),
    (["metrics", "contents", "PCT_90X"], 0),
    (["metrics", "contents", "PCT_100X"], 0),
    (["histogram", "contents", 0, "coverage"], 0),
    (["histogram", "contents", 0, "count"], 2860949724),
    (["histogram", "contents", -1, "coverage"], 250),
    (["histogram", "contents", -1, "count"], 0),
])
def test_wgs_v1124_01(wgs_v1124_01, attrs, exp):
    assert getattr_nested(wgs_v1124_01.json, attrs) == exp, \
        ", ".join([repr(x) for x in attrs])
