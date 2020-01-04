# -*- coding: utf-8 -*-
"""
    crimson.fastqc
    ~~~~~~~~~~~~~~

    FastQC output parsing.

"""
# (c) 2015-2020 Wibowo Arindrarto <bow@bow.web.id>

from io import StringIO
from os import PathLike, walk
from pathlib import Path
from typing import IO, Any, Dict, List, TextIO, Union, cast
from zipfile import ZipFile, is_zipfile

import click

from .utils import convert, get_handle

__all__ = ["parse"]

_MAX_SIZE = 1024 * 1024 * 10
_MAX_LINE_SIZE = 1024
_RESULTS_FNAME = "fastqc_data.txt"

# A module content can be a dictionary (when the module is 'Basic Statistics')
# or a list of dictionaries (keyed by the column name).
FastQCModuleContents = Union[Dict[str, Any], List[Dict[str, Any]]]

FastQCModulePayload = Dict[str, Union[str, FastQCModuleContents]]


class FastQCModule:

    """Class representing a FastQC analysis module."""

    def __init__(
        self,
        raw_lines: List[str],
        end_mark: str = ">>END_MODULE"
    ) -> None:
        """Initialize an instance.

        :param raw_lines: List of lines in the module.
        :param end_mark: Mark of the end of the module.

        """
        # The values of these will be set by _parse.
        self.status: str
        self.name: str

        self.extra: Dict[str, Any] = {}

        self.raw_lines = raw_lines
        self.end_mark = end_mark
        self.contents = self._parse()

    @property
    def dict(self) -> FastQCModulePayload:
        """Module data as a dictionary."""
        return {
            "contents": self.contents,
            "status": self.status,
            **self.extra,
        }

    def _parse(self) -> FastQCModuleContents:
        """Common parser for a FastQC module."""

        # Helper function for converting FastQC values that keeps
        # the "Base" column as strings (since it can be a number
        # or a strin denoting a range)
        def fqc_convert(k: str, v: Any) -> Any:
            if k == "Base":
                return v
            return convert(v)

        # check that the last line is a proper end mark
        if not self.raw_lines[-1].startswith(self.end_mark):
            raise ValueError(
                "Module last line does not start with the expected end mark"
                f" {self.end_mark!r}"
            )

        # parse name and status from first line
        tokens = self.raw_lines[0].strip().split("\t")
        name = tokens[0][2:]
        self.name = name
        status = tokens[-1]
        self.status = status
        # the rest of the lines except the last one
        lines = []
        if self.name != "Sequence Duplication Levels":
            # and column names from second/third line
            columns = self.raw_lines[1][1:].strip().split("\t")
            self._columns = columns
            for line in self.raw_lines[2:-1]:
                cols = line.strip().split("\t")
                lines.append(cols)
        else:
            extra_k, extra_v = self.raw_lines[1][1:].strip().split("\t")
            self.extra[extra_k] = convert(extra_v)
            columns = self.raw_lines[2][1:].strip().split("\t")
            self._columns = columns
            for line in self.raw_lines[3:-1]:
                cols = line.strip().split("\t")
                lines.append(cols)

        # optional processing for different modules
        if self.name == "Basic Statistics":
            return {k: convert(v) for k, v in lines}

        # try to convert numbers appropriately
        # except for "Base" column, since FastQC may output it as range
        return [
            {k: fqc_convert(k, v) for k, v in zpd}
            for zpd in [
                # zip column names and its values ~ each item in array ==
                # one row
                zip(columns, [v for v in d]) for d in lines
            ]
        ]


class FastQC:

    """Class representing results from a FastQC run."""

    _mod_names = [
        ">>Basic Statistics",
        ">>Per base sequence quality",
        ">>Per sequence quality scores",
        ">>Per base sequence content",
        ">>Per base GC content",
        ">>Per sequence GC content",
        ">>Per base N content",
        ">>Sequence Length Distribution",
        ">>Sequence Duplication Levels",
        ">>Overrepresented sequences",
        ">>Kmer Content",
    ]

    _mod_map = {k: k.lstrip(">") for k in _mod_names}

    def __init__(
        self,
        fp: TextIO,
        max_size: int = _MAX_SIZE,
        max_line_size: int = _MAX_LINE_SIZE,
    ) -> None:
        """Initialize an instance.

        :param fp: open file handle pointing to the FastQC data file
        :param max_size: Maximum allowed size of the FastQC data file (default:
            10 MiB).
        :param max_line_size: maximum number of bytes read everytime the
            underlying ``readline`` is called (default: 1024).

        """
        self.modules = {}
        self._max_line_size = _MAX_LINE_SIZE

        line = fp.readline(self._max_line_size)
        attr = ""
        read_size = self._max_line_size
        while read_size <= max_size:

            tokens = line.strip().split("\t")
            # break on EOF
            if not line:
                break
            # parse version
            elif line.startswith("##FastQC"):
                self.version = line.strip().split()[1]
            # parse individual modules
            elif tokens[0] in self._mod_map:
                attr = self._mod_map[tokens[0]]
                raw_lines = self._read_module(fp, line)
                self.modules[attr] = FastQCModule(raw_lines)

            line = fp.readline(self._max_line_size)
            read_size += self._max_line_size

    def _read_module(self, fp: TextIO, line: str) -> List[str]:
        """Return a list of lines in a module.

        :param fp: open file handle pointing to the FastQC data file
        :param line: first line in the module
        :returns: a list of lines in the module

        """
        raw = [line]
        while not line.startswith(">>END_MODULE"):
            line = fp.readline(self._max_line_size)
            raw.append(line)

            if not line:
                raise ValueError(f"Unexpected end of file in module {line!r}")

        return raw

    @property
    def dict(self) -> Dict[str, Union[str, FastQCModulePayload]]:
        """FastQC data as a dictionary."""
        payload: Dict[str, Union[str, FastQCModulePayload]]
        payload = {
            k: v.dict for k, v in self.modules.items()
        }
        payload["version"] = self.version

        return payload


def parse(
    in_data: Union[str, PathLike, IO],
    encoding: str = "utf-8",
    results_fname: str = _RESULTS_FNAME,
    max_size: int = _MAX_SIZE,
) -> dict:
    """Parses FastQC results into a dictionary.

    :param in_data: File handle of a fastqc_data.txt file, or path to a
        fastqc_data.txt file, or path to a FastQC results directory, or path to
        a zipped FastQC result.
    :param encoding: Encoding of the input file. This is ignored if ``in_data``
        is a file handle (default: utf-8).
    :param results_fname: Name of the text file produced by FastQC in which all
        the results are stored. This is ignored if ``in_data`` is a file handle
        (default: fastqc_data.txt).
    :param max_size: Maximum allowed size of the FastQC data file (default: 10
        MiB).
    :returns: Parsed FastQC values.

    """
    # Input is zipped FastQC result, extract data file contents into a file-like
    # handle and parse it.
    if is_zipfile(in_data):
        zf = ZipFile(in_data)
        try:
            data_fname, = [
                f for f in zf.namelist() if f.endswith(results_fname)
            ]
        except ValueError:
            raise click.BadParameter(
                f"File {in_data} contains an unexpected number of"
                f" files named {results_fname}."
            )

        with zf.open(data_fname) as src:
            data_contents = src.read(max_size).decode(encoding)

        fq = FastQC(StringIO(data_contents))

        return fq.dict

    # Make sure strings become Path instances.
    # Also, from this point on we only expect to see TextIO.
    in_data = cast(
        Union[Path, TextIO],
        Path(in_data) if isinstance(in_data, str) else in_data
    )

    # Input is FastQC directory.
    if isinstance(in_data, Path) and in_data.is_dir():
        try:
            ori = in_data
            in_data = ori.joinpath(
                next(walk(ori))[1][0],
                results_fname
            )
        except IndexError:
            raise click.BadParameter(
                f"Cannot find {results_fname} file in the given directory."
            )

    # Input is a fastqc_data.txt file handle or path to it.
    with get_handle(in_data, encoding=encoding) as fh:
        fq = FastQC(fh, max_size=max_size)

        return fq.dict
