# -*- coding: utf-8 -*-
"""
    crimson.utils
    ~~~~~~~~~~~~~

    General utilities.

"""
# (c) 2015-2020 Wibowo Arindrarto <bow@bow.web.id>

import json
import re
from contextlib import contextmanager
from os import PathLike, linesep
from pathlib import Path
from typing import IO, Generator, List, Optional, TextIO, Union

import click
import yaml

RE_INT = re.compile(r"^([-+]?\d+)L?$")
RE_FLOAT = re.compile(r"^([-+]?\d*\.?\d+(?:[eE][-+]?[0-9]+)?)$")


def convert(raw_str: str) -> Union[str, int, float]:
    """Tries to convert a string to an int, float, or return it unchanged.

    The function tries first to convert to an int. If it fails, it tries
    to convert to a float. If it fails, the origin input string is returned.

    :param raw_str: Input string.

    """
    maybe_int = RE_INT.search(raw_str)
    if maybe_int is not None:
        return int(maybe_int.group(1))

    maybe_float = RE_FLOAT.search(raw_str)
    if maybe_float is not None:
        return float(maybe_float.group(1))

    return raw_str


def write_output(
    payload: Union[dict, List[dict]],
    out_handle: TextIO,
    fmt: str = "json",
    compact: bool = False,
    indent: int = 4,
) -> None:
    """Writes the given dictionary as JSON or YAML to the output handle.

    :param payload: Payload to write.
    :param out_handle: Output handle.
    :param fmt: Output format.
    :param compact: Whether to write a compact JSON or not. Ignored if the
        output format is JSON.
    :param indent: Indentation level (ignored if output ``compact`` is true).

    """
    if fmt == "json":
        if compact:
            json.dump(
                payload,
                out_handle,
                sort_keys=True,
                indent=None,
                separators=(",", ":")
            )
        else:
            json.dump(payload, out_handle, sort_keys=True, indent=indent)
            out_handle.write(linesep)
    else:
        out_handle.write(
            yaml.dump(payload, default_flow_style=False, indent=indent)
        )


@contextmanager
def get_handle(
    input: Union[str, PathLike, IO],
    encoding: Optional[str] = None,
    mode: str = "r",
) -> Generator[TextIO, None, None]:
    """Context manager for opening files.

    This function returns a file handle of the given file name. You may also
    give an open file handle, in which case the file handle will be yielded
    immediately. The purpose of this is to allow the context manager handle
    both file objects and file names as inputs.

    If a file handle is given, it is not closed upon exiting the context.
    If a file name is given, it will be closed upon exit.

    :param input: Handle of open file or file name.
    :param encoding: Encoding of the file. Ignored if input is file handle.
    :param mode: Mode for opening file. Ignored if input is file handle.

    """
    if isinstance(input, (str, Path)):
        fh = click.open_file(f"{input}", mode=mode, encoding=encoding)
    else:
        fh = input

    yield fh

    if isinstance(input, str):
        fh.close()
