# -*- coding: utf-8 -*-
"""
    crimson.tests.utils
    ~~~~~~~~~~~~~~~~~~~

    General test utilities.

"""
# (c) 2015-2018 Wibowo Arindrarto <bow@bow.web.id>
from os.path import abspath, dirname, join


TEST_CASE_DIR = abspath(join(dirname(__file__), "cases"))


def get_test_path(bname, test_dir=TEST_CASE_DIR):
    """Helper method to return the path of a test case file or directory.

    :param bname: Test case base name.
    :type bname: str
    :param test_dir: Test case directory name.
    :type test_dir: str
    :returns: Absolute path to the test case file or directory.
    :rtype: str

    """
    return abspath(join(test_dir, bname))


def getattr_nested(obj, idxs):
    """Helper method for recursively fetching an item from the given object.

    :param obj: Object containing the item to retrieve.
    :type obj: object
    :param idxs: List of attribute names / indices / keys to retrieve the item.
    :type idxs: list(str, int)
    :returns: None or the item.

    """
    if len(idxs) == 0:
        return obj

    idx = idxs.pop(0)

    if isinstance(obj, dict):
        if idx in obj:
            return getattr_nested(obj[idx], idxs)
    elif isinstance(obj, (list, tuple)) and isinstance(idx, int):
        if idx < len(obj):
            return getattr_nested(obj[idx], idxs)
    else:
        return getattr_nested(getattr(obj, idx))
