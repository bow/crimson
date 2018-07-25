# -*- coding: utf-8 -*-
"""
    fusioncatcher subcommand tests
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
# (c) 2015-2018 Wibowo Arindrarto <bow@bow.web.id>
import json
import pytest
from click.testing import CliRunner

from crimson.cli import main

from .utils import get_test_path, getattr_nested


@pytest.fixture(scope="module")
def fusioncatcher_fail():
    runner = CliRunner()
    in_file = get_test_path("fusioncatcher_nope.txt")
    result = runner.invoke(main, ["fusioncatcher", in_file])
    return result


@pytest.fixture(scope="module")
def fusioncatcher_v0995a():
    runner = CliRunner()
    in_file = get_test_path("fusioncatcher_v0995a.txt")
    result = runner.invoke(main, ["fusioncatcher", in_file])
    result.json = json.loads(result.output)
    return result


def test_fusioncatcher_fail_exit_code(fusioncatcher_fail):
    assert fusioncatcher_fail.exit_code != 0


def test_fusioncatcher_fail_output(fusioncatcher_fail):
    err_msg = "Unexpected column names:"
    assert err_msg in fusioncatcher_fail.output


@pytest.mark.parametrize("attrs, exp", [
    ([0, "5end", "geneSymbol"], "RUNX1"),
    ([0, "5end", "geneID"], "ENSG00000159216"),
    ([0, "5end", "exonID"], "ENSE00003512550"),
    ([0, "5end", "chromosome"], "21"),
    ([0, "5end", "position"], 34859474),
    ([0, "5end", "strand"], "-"),
    ([0, "3end", "geneSymbol"], "RUNX1T1"),
    ([0, "3end", "geneID"], "ENSG00000079102"),
    ([0, "3end", "exonID"], "ENSE00003614817"),
    ([0, "3end", "chromosome"], "8"),
    ([0, "3end", "position"], 92017363),
    ([0, "3end", "strand"], "-"),
    ([0, "fusionDescription"], ["known", "chimerdb2", "ticdb", "tcga",
                                "cell_lines"]),
    ([0, "nCommonMappingReads"], 0),
    ([0, "nSpanningPairs"], 41),
    ([0, "nSpanningUniqueReads"], 16),
    ([0, "longestAnchorLength"], 62),
    ([0, "fusionFindingMethod"], ["BOWTIE", "BOWTIE+BLAT", "BOWTIE+STAR"]),
    ([0, "fusionSequence"],
        "CTACCACAGAGCCATCAAAATCACAGTGGATGGGCCCCGAGAACCTCGAA*ATCGTACTGAGAAGCA"
        "CTCCACAATGCCAGACTCACCTGTGGATGTGAAG"),
    ([0, "predictedEffect"], "in-frame"),
    ([0, "predictedFusedTranscripts", 0],
        "ENST00000437180:803/ENST00000522467:311"),
    ([0, "predictedFusedTranscripts", -1],
        "ENST00000344691:2110/ENST00000518992:377"),
    ([0, "predictedFusedProteins", 0],
        "MASDSIFESFPSYPQCFMRECILGMNPSRDVHDASTSRRFTPPSTALSPGKMSEALPLGAPDAGAAL"
        "AGKLRSGDRSMVEVLADHPGELVRTDSPNFLCSVLPTHWRCNKTLPIAFKVVALGDVPDGTLVTVMA"
        "GNDENYSAELRNATAAMKNQVARFNDLRFVGRSGRGKSFTLTITVFTNPPQVATYHRAIKITVDGPR"
        "EPRNRTEKHSTMPDSPVDVKTQSRLTPPTMPPPPTTQGAPRTSSFTPTTLTNGTSHSPTALNGAPSP"
        "PNGFSNGPSSSSSSSLANQQLPPACGARQLSKLKRFLTTLQQFGNDISPEIGERVRTLVLGLV"),
    ([0, "predictedFusedProteins", -1],
        "MRIPVDASTSRRFTPPSTALSPGKMSEALPLGAPDAGAALAGKLRSGDRSMVEVLADHPGELVRTDS"
        "PNFLCSVLPTHWRCNKTLPIAFKVVALGDVPDGTLVTVMAGNDENYSAELRNATAAMKNQVARFNDL"
        "RFVGRSGRGKSFTLTITVFTNPPQVATYHRAIKITVDGPREPRNRTEKHSTMPDSPVDVKTQSRLTP"
        "PTMPPPPTTQGAPRTSSFTPTTLTNGTSHSPTALNGAPSPPNGFSNGPSSSSSSSLANQQLPPACGA"
        "RQLSKLKRFLTTLQQFGNDISPEIGERVRTLVLGLVNSTLTIEEFHSKLQEATNFPLRPFVIPFLKA"
        "NLPLLQRELLHCARLAKQNPAQYLAQHEQLLLDASTTSPVDS"),

    ([-1, "5end", "geneSymbol"], "VPS45"),
    ([-1, "5end", "geneID"], "ENSG00000136631"),
    ([-1, "5end", "exonID"], "ENSE00003679462"),
    ([-1, "5end", "chromosome"], "1"),
    ([-1, "5end", "position"], 150110627),
    ([-1, "5end", "strand"], "+"),
    ([-1, "3end", "geneSymbol"], "PLEKHO1"),
    ([-1, "3end", "geneID"], "ENSG00000023902"),
    ([-1, "3end", "exonID"], "ENSE00003616995"),
    ([-1, "3end", "chromosome"], "1"),
    ([-1, "3end", "position"], 150150912),
    ([-1, "3end", "strand"], "+"),
    ([-1, "fusionDescription"], ["adjacent", "known", "healthy", "hpa",
                                 "banned", "1K<gap<10K", "readthrough"]),
    ([-1, "nCommonMappingReads"], 0),
    ([-1, "nSpanningPairs"], 1),
    ([-1, "nSpanningUniqueReads"], 3),
    ([-1, "longestAnchorLength"], 29),
    ([-1, "fusionFindingMethod"], ["BOWTIE"]),
    ([-1, "fusionSequence"],
        "TGAGGATTGTCCTGGGAGGCACCACAGTGCACAACACGAAAAG*"
        "GGACCTCAGGATGGAAACCAGCAGCCTGCACCGCCCGAGAAGG"),
    ([-1, "predictedEffect"], "out-of-frame"),
    ([-1, "predictedFusedTranscripts", 0],
        "ENST00000369128:1550/ENST00000369124:309"),
    ([-1, "predictedFusedTranscripts", -1],
        "ENST00000369130:2171/ENST00000369124:309"),
    ([-1, "predictedFusedProteins", 0],
        "MVYTQSEILQKEVYLFERIDSQNREIMKHLKAICFLRPTKENVDYIIQELRRPKYTIYFIYFSNVISK"
        "SDVKSLAEADEQEVVAEVQQVITKEYELFEFRRTEVPPLLLILDRCDDAITPLLNQWTYQAMVHELLG"
        "INNNRIDLSRVPGISKDLREVVLSAENDEFYANNMYLNFAEIGSNIKNLMEDFQKKKPKEQQKLESIA"
        "DMKAFVENYPQFKKMSGTVSKHVTVVGELSRLVSERNLLEVSEVEQELACQNDHSSALQNIKRLLQNP"
        "KVTEFDAARLVMLYALHYERHSSNSLPGLMMDLRNKGVSEKYRKLVSAVVEYGGKRVRGSDLFSPKDA"
        "VAITKQFLKGLKGVENVYTQHQPFLHETLDHLIKGRLKENLYPYLGPSTLRDRPQDIIVFVIGGATYE"
        "EALTVYNLNRTTPGVRIVLGGTTVHNTKRDLRMETSSLHRPRRSAGSGNSAGKGFSGRFGKTAMWC"),
    ([-1, "predictedFusedProteins", -1],
        "MNVVFAVKQYISKMIEDSGPGMKVLLMDKETTGIVSMVYTQSEILQKEVYLFERIDSQNREIMKHLKA"
        "ICFLRPTKENVDYIIQELRRPKYTIYFIYFSNVISKSDVKSLAEADEQEVVAEVQEFYGDYIAVNPHL"
        "FSLNILGCCQGRNWDPAQLSRTTQGLTALLLSLKKCPMIRYQLSSEAAKRLAECVKQVITKEYELFEF"
        "RRTEVPPLLLILDRCDDAITPLLNQWTYQAMVHELLGINNNRIDLSRVPGISKDLREVVLSAENDEFY"
        "ANNMYLNFAEIGSNIKNLMEDFQKKKPKEQQKLESIADMKAFVENYPQFKKMSGTVSKHVTVVGELSR"
        "LVSERNLLEVSEVEQELACQNDHSSALQNIKRLLQNPKVTEFDAARLVMLYALHYERHSSNSLPGLMM"
        "DLRNKGVSEKYRKLVSAVVEYGGKRVRGSDLFSPKDAVAITKQFLKGLKGVENVYTQHQPFLHETLDH"
        "LIKGRLKENLYPYLGPSTLRDRPQDIIVFVIGGATYEEALTVYNLNRTTPGVRIVLGGTTVHNTKRDL"
        "RMETSSLHRPRRSAGSGNSAGKGFSGRFGKTAMWC"),
])
def test_fusioncatcher_v0995a(fusioncatcher_v0995a, attrs, exp):
    assert getattr_nested(fusioncatcher_v0995a.json, attrs) == exp, \
        ", ".join([repr(x) for x in attrs])
