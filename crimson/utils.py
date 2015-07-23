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
from os import linesep


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


def write_json(payload, out_handle, compact=False, indent=4):
    """Writes the given dictionary as JSON to the output handle.

    The output handle must have the ``write`` method.

    :param payload: JSON payload to write.
    :type payload: dict
    :param out_handle: Output handle.
    :type out_handle: object with ``write`` method.
    :param compact: Whether to write a compact JSON or not.
    :type compact: bool
    :param indent: JSON indentation (ignored if output ``compact`` is true).
    :type indent: int

    """
    if compact:
        json.dump(payload, out_handle, sort_keys=True, indent=None,
                  separators=(",", ":"))
    else:
        json.dump(payload, out_handle, sort_keys=True, indent=indent)
        out_handle.write(linesep)
