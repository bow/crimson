# -*- coding: utf-8 -*-
"""
    crimson.fastqc
    ~~~~~~~~~~~~~~

    FastQC output parsing.

    :copyright: (c) 2015 Wibowo Arindrarto <bow@bow.web.id>
    :license: BSD

"""
from os import path, walk

import click

from .utils import convert, get_handle


__all__ = ["parse"]


_MAX_LINE_SIZE = 1024


class FastQCModule(object):

    """Class representing a FastQC analysis module."""

    def __init__(self, raw_lines, end_mark='>>END_MODULE'):
        """

        :param raw_lines: list of lines in the module
        :type raw_lines: list of str
        :param end_mark: mark of the end of the module
        :type end_mark: str

        """
        self.extra = {}
        self.raw_lines = raw_lines
        self.end_mark = end_mark
        self.status = None
        self.name = None
        self.contents = self._parse()

    @property
    def dict(self):
        """Module data as a dictionary."""
        payload = {
            "contents": self.contents,
            "status": self.status
        }
        if len(self.extra) > 0:
            for ek, ev in self.extra.items():
                payload[ek] = ev
        return payload

    def _parse(self):
        """Common parser for a FastQC module."""

        # Helper function for converting FastQC values that keeps
        # the "Base" column as strings (since it can be a number
        # or a strin denoting a range)
        def fqc_convert(k, v):
            if k == "Base":
                return v
            return convert(v)

        # check that the last line is a proper end mark
        assert self.raw_lines[-1].startswith(self.end_mark)
        # parse name and status from first line
        tokens = self.raw_lines[0].strip().split('\t')
        name = tokens[0][2:]
        self.name = name
        status = tokens[-1]
        self.status = status
        # the rest of the lines except the last one
        data = []
        if self.name != "Sequence Duplication Levels":
            # and column names from second/third line
            columns = self.raw_lines[1][1:].strip().split("\t")
            self._columns = columns
            for line in self.raw_lines[2:-1]:
                cols = line.strip().split("\t")
                data.append(cols)
        else:
            extra_k, extra_v = self.raw_lines[1][1:].strip().split("\t")
            self.extra[extra_k] = convert(extra_v)
            columns = self.raw_lines[2][1:].strip().split("\t")
            self._columns = columns
            for line in self.raw_lines[3:-1]:
                cols = line.strip().split("\t")
                data.append(cols)

        # optional processing for different modules
        if self.name == 'Basic Statistics':
            data = {k: convert(v) for k, v in data}
        else:
            # zip column names and its values ~ each item in array == one row
            data = [zip(columns, [v for v in d]) for d in data]
            # try to convert numbers appropriately
            # except for "Base" column, since FastQC may output it as range
            data = [{k: fqc_convert(k, v) for k, v in zpd} for zpd in data]

        return data


class FastQC(object):

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

    def __init__(self, fp):
        """

        :param fp: open file handle pointing to the FastQC data file
        :type fp: file handle

        """
        self.modules = {}

        line = fp.readline(_MAX_LINE_SIZE)
        attr = ""
        while True:

            tokens = line.strip().split('\t')
            # break on EOF
            if not line:
                break
            # parse version
            elif line.startswith('##FastQC'):
                self.version = line.strip().split()[1]
            # parse individual modules
            elif tokens[0] in self._mod_map:
                attr = self._mod_map[tokens[0]]
                raw_lines = self._read_module(fp, line)
                self.modules[attr] = FastQCModule(raw_lines)

            line = fp.readline(_MAX_LINE_SIZE)

    def _read_module(self, fp, line):
        """Returns a list of lines in a module.

        :param fp: open file handle pointing to the FastQC data file
        :type fp: file handle
        :param line: first line in the module
        :type line: str
        :returns: a list of lines in the module
        :rtype: list of str

        """
        raw = [line]
        while not line.startswith('>>END_MODULE'):
            line = fp.readline(_MAX_LINE_SIZE)
            raw.append(line)

            if not line:
                raise ValueError("Unexpected end of file in module %r" % line)

        return raw

    @property
    def dict(self):
        """FastQC data as a dictionary."""
        payload = {k: v.dict for k, v in self.modules.items()}
        payload["version"] = self.version
        return payload


def parse(in_data):
    """Parses FastQC results into a dictionary.

    :param in_data: File handle of a fastqc_data.txt file, or path to a
                    fastqc_data.txt file or path to a FastQC results directory.
    :type in_data: str or file handle
    :returns: Parsed FastQC values.
    :rtype: dict

    """
    if path.isdir(in_data):
        try:
            ori = in_data
            in_data = path.join(ori, next(walk(ori))[1][0], "fastqc_data.txt")
        except IndexError:
            raise click.BadParameter("Cannot find fastqc_data.txt file in "
                                     "the given directory.")
    with get_handle(in_data) as fh:
        return FastQC(fh).dict
