# -*- coding: utf-8 -*-
"""
    crimson.tests.utils
    ~~~~~~~~~~~~~~~~~~~

    General test utilities.

    :copyright: (c) 2015 Wibowo Arindrarto <bow@bow.web.id>
    :license: BSD

"""
from os.path import abspath, dirname, join


TEST_CASE_DIR = abspath(join(dirname(__file__), "cases"))


def get_test_file(bname, test_dir=TEST_CASE_DIR):
    return abspath(join(test_dir, bname))
