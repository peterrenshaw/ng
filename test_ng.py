#!/usr/bin/env python
# ~*~ encoding: utf-8 ~*~


#---
# copy: copyright (C) 2013 Peter Renshaw
#---


import json
import os.path
import unittest


import ng


class TestNg(unittest.TestCase):
    def setUp(self):
        self.n = ng.Nextgen()
        self.source_dir = os.getcwd()
    def tearDown(self):
        self.n = None


    # init
    def test_ng_init(self):
        self.assertTrue(self.n)

    # source
    def test_ng_source_ok(self):
        self.assertTrue(self.n.source(self.source_dir))
    def test_ng_source_fail(self):
        self.assertFalse(self.n.source(""))

    # read
    def test_ng_read_ok(self):
        self.n.source(self.source_dir)
        self.assertTrue(self.n.read())
    def test_ng_read_fail(self):
        self.n.source("")
        self.assertFalse(self.n.read())
    def test_ng_filepath_ok(self):
        self.n.source(self.source_dir)
        self.n.read()
        self.assertTrue(len(self.n.filepath) > 0)

    # destination
    

    # process
#---
# suite: allows all tests run here to be run externally at 'test_all.py'
#---
def suite():
    """tests added to run in 'test_all.py'"""
    tests = ['test_ng_init',
             'test_ng_source_ok',
             'test_ng_source_fail']

    return unittest.TestSuite(map(TestNg, tests))


if __name__ == "__main__":
    suite()
    unittest.main()


# vim: ff=unix:ts=4:sw=4:tw=78:noai:expandtab
