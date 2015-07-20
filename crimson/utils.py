# -*- coding: utf-8 -*-
"""
    crimson.utils
    ~~~~~~~~~~~~~

    General utilities.

    :copyright: (c) 2015 Wibowo Arindrarto <bow@bow.web.id>
    :license: BSD

"""
import json
from os import linesep


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
