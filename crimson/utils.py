# -*- coding: utf-8 -*-
"""
    crimson.utils
    ~~~~~~~~~~~~~

    General utilities.

    :copyright: (c) 2015 Wibowo Arindrarto <bow@bow.web.id>
    :license: BSD

"""
import json
import re
import sys
from contextlib import contextmanager
from os import linesep

import click
import yaml


if sys.version_info[0] > 2:
    basestring = str


RE_INT = re.compile(r"^([-+]?\d+)L?$")
RE_FLOAT = re.compile(r"^([-+]?\d*\.?\d+(?:[eE][-+]?[0-9]+)?)$")


def convert(raw_str):
    """Tries to convert a string to an int, float, or return it unchanged.

    The function tries first to convert to an int. If it fails, it tries
    to convert to a float. If it fails, the origin input string is returned.

    :param raw_str: Input string.
    :type raw_str: str

    """
    maybe_int = RE_INT.search(raw_str)
    if maybe_int is not None:
        return int(maybe_int.group(1))
    maybe_float = RE_FLOAT.search(raw_str)
    if maybe_float is not None:
        return float(maybe_float.group(1))
    return raw_str


def write_output(payload, out_handle, fmt="json", compact=False, indent=4):
    """Writes the given dictionary as JSON or YAML to the output handle.

    The output handle must have the ``write`` method.

    :param payload: Payload to write.
    :type payload: dict
    :param out_handle: Output handle.
    :type out_handle: object with ``write`` method.
    :param fmt: Output format.
    :type fmt: str (``json`` or ``yaml``)
    :param compact: Whether to write a compact JSON or not. Ignored if the
                    output format is JSON.
    :type compact: bool
    :param indent: Indentation level (ignored if output ``compact`` is true).
    :type indent: int

    """
    if fmt == "json":
        if compact:
            json.dump(payload, out_handle, sort_keys=True, indent=None,
                      separators=(",", ":"))
        else:
            json.dump(payload, out_handle, sort_keys=True, indent=indent)
            out_handle.write(linesep)
    else:
        out_handle.write(yaml.dump(payload, default_flow_style=False,
                         indent=indent))


@contextmanager
def get_handle(input, encoding=None, mode="r"):
    """Context manager for opening files.

    This function returns a file handle of the given file name. You may also
    give an open file handle, in which case the file handle will be yielded
    immediately. The purpose of this is to allow the context manager handle
    both file objects and file names as inputs.

    If a file handle is given, it is not closed upon exiting the context.
    If a file name is given, it will be closed upon exit.

    :param input: Handle of open file or file name.
    :type input: file handle or obj
    :param encoding: Encoding of the file. Ignored if input is file handle.
    :type encoding: str
    :param mode: Mode for opening file. Ignored if input is file handle.
    :type mode: str

    """
    if isinstance(input, basestring):
        assert isinstance(input, basestring), \
            "Unexpected input type: " + repr(input)
        fh = click.open_file(input, mode=mode, encoding=encoding)
    else:
        fh = input

    yield fh

    if isinstance(input, basestring):
        fh.close()
