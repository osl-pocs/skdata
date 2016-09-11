#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_vizpydata
----------------------------------

Tests for `vizpydata` module.
"""


import sys
import unittest
from contextlib import contextmanager

from vizpydata.widgets import DataAnalysisWidget
from vizpydata.utils import cross_fields, summary, make_chart



class Testvizpydata(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_000_something(self):
        pass

if __name__ == '__main__':
    sys.exit(unittest.main())
