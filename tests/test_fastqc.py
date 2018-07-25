# -*- coding: utf-8 -*-
"""
    fastqc subcommand tests
    ~~~~~~~~~~~~~~~~~~~~~~~

"""
# (c) 2015-2018 Wibowo Arindrarto <bow@bow.web.id>
import json
import os

import pytest
from click.testing import CliRunner

from crimson.cli import main
from .utils import get_test_path, getattr_nested


def test_fastqc_dir_error():
    runner = CliRunner()
    result = runner.invoke(main, ["fastqc", os.getcwd()])
    assert result.exit_code != 0


@pytest.fixture(scope="module")
def fastqc_fail():
    runner = CliRunner()
    in_file = get_test_path("fastqc_nope.txt")
    result = runner.invoke(main, ["fastqc", in_file])
    return result


def test_fastqc_fail(fastqc_fail):
    assert fastqc_fail.exit_code == -1


@pytest.fixture(scope="module")
def fastqc_v0101_01():
    runner = CliRunner()
    in_file = get_test_path("fastqc_v0101_01.txt")
    result = runner.invoke(main, ["fastqc", in_file])
    result.json = json.loads(result.output)
    return result


def test_fastqc_v0101_01_exit_code(fastqc_v0101_01):
    assert fastqc_v0101_01.exit_code == 0


@pytest.mark.parametrize("attrs, exp", [
    (["version"], "0.10.1"),
])
def test_fastqc_v0101_01_root(fastqc_v0101_01, attrs, exp):
    # since the function call modifies the list
    ori_attrs = list(attrs)
    assert getattr_nested(fastqc_v0101_01.json, attrs) == exp, \
        ", ".join([repr(x) for x in ori_attrs])


@pytest.mark.parametrize("attrs, exp", [
    (["status"], "pass"),
    (["contents", "Filename"], "/home/crimson/fastqc/input.fq.gz"),
    (["contents", "File type"], "Conventional base calls"),
    (["contents", "Encoding"], "Sanger / Illumina 1.9"),
    (["contents", "Total Sequences"], 7154316),
    (["contents", "Filtered Sequences"], 0),
    (["contents", "Sequence length"], 125),
    (["contents", "%GC"], 48),
])
def test_fastqc_v0101_01_basic_statistics(fastqc_v0101_01, attrs, exp):
    attrs = ["Basic Statistics"] + attrs
    ori_attrs = list(attrs)
    assert getattr_nested(fastqc_v0101_01.json, attrs) == exp, \
        ", ".join([repr(x) for x in ori_attrs])


@pytest.mark.parametrize("attrs, exp", [
    (["status"], "pass"),
    (["contents", 0, "Base"], "1"),
    (["contents", 0, "Mean"], 26.173029818643737),
    (["contents", 0, "Median"], 28.0),
    (["contents", 0, "Lower Quartile"], 18.0),
    (["contents", 0, "Upper Quartile"], 32.0),
    (["contents", 0, "10th Percentile"], 18.0),
    (["contents", 0, "90th Percentile"], 33.0),
    (["contents", 124, "Base"], "125"),
    (["contents", 124, "Mean"], 33.835322482261056),
    (["contents", 124, "Median"], 38.0),
    (["contents", 124, "Lower Quartile"], 35.0),
    (["contents", 124, "Upper Quartile"], 38.0),
    (["contents", 124, "10th Percentile"], 25.0),
    (["contents", 124, "90th Percentile"], 38.0),
    (["contents", 125], None),
])
def test_fastqc_v0101_01_base_sequence_quality(fastqc_v0101_01, attrs, exp):
    attrs = ["Per base sequence quality"] + attrs
    ori_attrs = list(attrs)
    assert getattr_nested(fastqc_v0101_01.json, attrs) == exp, \
        ", ".join([repr(x) for x in ori_attrs])


@pytest.mark.parametrize("attrs, exp", [
    (["status"], "pass"),
    (["contents", 0, "Quality"], 2),
    (["contents", 0, "Count"], 522.0),
    (["contents", 35, "Quality"], 37),
    (["contents", 35, "Count"], 4126023.0),
    (["contents", 36], None),
])
def test_fastqc_v0101_01_sequence_quality_scores(fastqc_v0101_01, attrs, exp):
    attrs = ["Per sequence quality scores"] + attrs
    ori_attrs = list(attrs)
    assert getattr_nested(fastqc_v0101_01.json, attrs) == exp, \
        ", ".join([repr(x) for x in ori_attrs])


@pytest.mark.parametrize("attrs, exp", [
    (["status"], "fail"),
    (["contents", 0, "Base"], "1"),
    (["contents", 0, "G"], 45.23537595867585),
    (["contents", 0, "A"], 16.85510270835236),
    (["contents", 0, "T"], 12.633971292200583),
    (["contents", 0, "C"], 25.27555004077121),
    (["contents", 124, "Base"], "125"),
    (["contents", 124, "G"], 24.28912421870512),
    (["contents", 124, "A"], 25.548183619130793),
    (["contents", 124, "T"], 25.64126039286254),
    (["contents", 124, "C"], 24.52143176930155),
    (["contents", 125], None),
])
def test_fastqc_v0101_01_base_sequence_content(fastqc_v0101_01, attrs, exp):
    attrs = ["Per base sequence content"] + attrs
    ori_attrs = list(attrs)
    assert getattr_nested(fastqc_v0101_01.json, attrs) == exp, \
        ", ".join([repr(x) for x in ori_attrs])


@pytest.mark.parametrize("attrs, exp", [
    (["status"], "fail"),
    (["contents", 0, "Base"], "1"),
    (["contents", 0, "%GC"], 70.51092599944707),
    (["contents", 124, "Base"], "125"),
    (["contents", 124, "%GC"], 48.81055598800667),
    (["contents", 125], None),
])
def test_fastqc_v0101_01_base_gc(fastqc_v0101_01, attrs, exp):
    attrs = ["Per base GC content"] + attrs
    ori_attrs = list(attrs)
    assert getattr_nested(fastqc_v0101_01.json, attrs) == exp, \
        ", ".join([repr(x) for x in ori_attrs])


@pytest.mark.parametrize("attrs, exp", [
    (["status"], "warn"),
    (["contents", 0, "GC Content"], 0),
    (["contents", 0, "Count"], 2.0),
    (["contents", 100, "GC Content"], 100),
    (["contents", 100, "Count"], 0.0),
    (["contents", 101], None),
])
def test_fastqc_v0101_01_sequence_gc(fastqc_v0101_01, attrs, exp):
    attrs = ["Per sequence GC content"] + attrs
    ori_attrs = list(attrs)
    assert getattr_nested(fastqc_v0101_01.json, attrs) == exp, \
        ", ".join([repr(x) for x in ori_attrs])


@pytest.mark.parametrize("attrs, exp", [
    (["status"], "pass"),
    (["contents", 0, "Base"], "1"),
    (["contents", 0, "N-Count"], 0.0480409308171459),
    (["contents", 124, "Base"], "125"),
    (["contents", 124, "N-Count"], 9.784303628746619e-5),
    (["contents", 125], None),
])
def test_fastqc_v0101_01_base_n_content(fastqc_v0101_01, attrs, exp):
    attrs = ["Per base N content"] + attrs
    ori_attrs = list(attrs)
    assert getattr_nested(fastqc_v0101_01.json, attrs) == exp, \
        ", ".join([repr(x) for x in ori_attrs])


@pytest.mark.parametrize("attrs, exp", [
    (["status"], "pass"),
    (["contents", 0, "Length"], 125),
    (["contents", 0, "Count"], 7154316.0),
    (["contents", 1], None),
])
def test_fastqc_v0101_01_length_distribution(fastqc_v0101_01, attrs, exp):
    attrs = ["Sequence Length Distribution"] + attrs
    ori_attrs = list(attrs)
    assert getattr_nested(fastqc_v0101_01.json, attrs) == exp, \
        ", ".join([repr(x) for x in ori_attrs])


@pytest.mark.parametrize("attrs, exp", [
    (["status"], "fail"),
    (["Total Duplicate Percentage"], 66.47973811024582),
    (["contents", 0, "Duplication Level"], 1),
    (["contents", 0, "Relative count"], 100.0),
    (["contents", 9, "Duplication Level"], "10++"),
    (["contents", 9, "Relative count"], 37.5636919493376),
    (["contents", 10], None),
])
def test_fastqc_v0101_01_duplication_levels(fastqc_v0101_01, attrs, exp):
    attrs = ["Sequence Duplication Levels"] + attrs
    ori_attrs = list(attrs)
    assert getattr_nested(fastqc_v0101_01.json, attrs) == exp, \
        ", ".join([repr(x) for x in ori_attrs])


@pytest.mark.parametrize("attrs, exp", [
    (["status"], "pass"),
    (["contents", 0], None),
])
def test_fastqc_v0101_01_overrepresented(fastqc_v0101_01, attrs, exp):
    attrs = ["Overrepresented sequences"] + attrs
    ori_attrs = list(attrs)
    assert getattr_nested(fastqc_v0101_01.json, attrs) == exp, \
        ", ".join([repr(x) for x in ori_attrs])


@pytest.mark.parametrize("attrs, exp", [
    (["status"], "warn"),
    (["contents", 0, "Sequence"], "TTTTT"),
    (["contents", 0, "Count"], 3280715),
    (["contents", 0, "Obs/Exp Overall"], 3.415043),
    (["contents", 0, "Obs/Exp Max"], 5.682842),
    (["contents", 0, "Max Obs/Exp Position"], 25),
    (["contents", 93, "Sequence"], "GTACG"),
    (["contents", 93, "Count"], 370820),
    (["contents", 93, "Obs/Exp Overall"], 0.4485244),
    (["contents", 93, "Obs/Exp Max"], 6.9574623),
    (["contents", 93, "Max Obs/Exp Position"], 14),
    (["contents", 94], None),
])
def test_fastqc_v0101_01_kmer_content(fastqc_v0101_01, attrs, exp):
    attrs = ["Kmer Content"] + attrs
    ori_attrs = list(attrs)
    assert getattr_nested(fastqc_v0101_01.json, attrs) == exp, \
        ", ".join([repr(x) for x in ori_attrs])


def test_fastqc_v0101_01_dir():
    runner = CliRunner()
    dir_name = "fastqc_v0101_01_dir.fastqc"
    dir_path = get_test_path(dir_name)
    dir_result = runner.invoke(main, ["fastqc", dir_path])

    file_name = "fastqc_v0101_01_dir.fastqc/input.fq_fastqc/fastqc_data.txt"
    file_path = get_test_path(file_name)
    file_result = runner.invoke(main, ["fastqc", file_path])

    assert dir_result.output == file_result.output


def test_fastqc_v0101_02_zip():
    runner = CliRunner()
    zip_path = get_test_path("fastqc_v0101_02.fq_fastqc.zip")
    zip_result = runner.invoke(main, ["fastqc", zip_path])

    data_path = get_test_path("fastqc_v0101_02.txt")
    data_result = runner.invoke(main, ["fastqc", data_path])

    assert data_result.output
    assert data_result.output == zip_result.output


@pytest.fixture(scope="module")
def fastqc_zip_not_fastqc():
    runner = CliRunner()
    in_file = get_test_path("fastqc_not_fastqc.zip")
    result = runner.invoke(main, ["fastqc", in_file])
    return result


def test_fastqc_zip_not_fastqc(fastqc_zip_not_fastqc):
    assert fastqc_zip_not_fastqc.exit_code != 0
    print(dir(fastqc_zip_not_fastqc))
    assert "contains an unexpected number of" in fastqc_zip_not_fastqc.output
