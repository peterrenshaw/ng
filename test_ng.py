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
    def tearDown(self):
        self.n = None


    def test_ng_init(self):
        self.assertTrue(self.n)
    def test_ng_source_ok(self):
        source_dir = os.getcwd()
        self.assertTrue(self.n.source(source_dir))
    def test_ng_source_fail(self):
        self.assertFalse(self.n.source(""))
        

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
