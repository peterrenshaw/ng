#!/usr/bin/env python
# ~*~ encoding: utf-8 ~*~


#---
# copy: copyright (C) 2013 Peter Renshaw
#---


import os.path
import unittest


import ng


class TestNg(unittest.TestCase):
    def setUp(self):
        self.n = ng.Nextgen()
        self.source_dir = os.getcwd()
        self.source_dir_fail = os.path.join(self.source_dir, 'foo')
    def tearDown(self):
        self.n = None
        self.soruce_dir = None
        self.source_dir_fail = None


    # init
    def test_ng_init(self):
        self.assertTrue(self.n)

    # directory
    def test_is_dir_valid_ok(self):
        self.assertTrue(self.n.is_dir_valid(self.source_dir))
    def test_is_dir_valid_fail(self):
        self.assertFalse(self.n.is_dir_valid(self.source_dir_fail))
    def test_ng_source_ok(self):
        self.assertTrue(self.n.source(self.source_dir))
    def test_ng_source_fail(self):
        self.assertFalse(self.n.source(""))
    def test_ng_dest_ok(self):
        self.assertTrue(self.n.destination(self.source_dir))
    def test_ng_dest_fail(self):
        self.assertFalse(self.n.destination(self.source_dir_fail))


    # read
    def test_ng_read_ok(self):
        self.n.source(self.source_dir)
        status = self.n.read()
        self.assertTrue(status != False)
    def test_ng_read_fail(self):
        self.n.source("")
        self.assertFalse(self.n.read())
    def test_ng_filepath_ok(self):
        self.n.source(self.source_dir)
        if self.n.read():
            self.assertTrue(len(self.n.filepath) > 0)
        else:
            self.assertTrue(False)
    def test_ng_filepath_fail(self):
        pass

    # yaml
    def test_extract_yaml_ok(self):
        pass
    def test_extract_yaml_fail(self):
        pass
    def test_extract_yaml_tags_ok(self):
        pass
    def test_extract_yaml_tags_fail(self):
        pass
    def test_extract_yaml_date_ok(self):
        pass
    def test_extract_yaml_date_fail(self):
        pass
    # tags
    def test_update_tags_ok(self):
        """remember, tag list returns unchanged, even on failure"""
        tag = "today"
        tags = []
        self.assertEqual(self.n.update_tags(tag, tags),['today'])
    def test_update_tags_fail(self):
        """remember, tags list returns unchanged, even on failure"""
        tag = "today"
        tags = ['today']
        self.assertEqual(self.n.update_tags(tag, tags),tags)
    # read
    def test_read_ok(self):
        # valid directory, not file!!!
        #rok = self.n.read(self.source_dir)
        #self.assertTrue(rok)
        pass
    def test_read_fail(self):
        rof = self.n.read("")
        self.assertFalse(rof)

    # process
#---
# suite: allows all tests run here to be run externally at 'test_all.py'
#---
def suite():
    """tests added to run in 'test_all.py'"""
    tests = ['test_ng_init',
             'test_ng_source_ok',
             'test_ng_source_fail',
             'test_is_dir_valid_ok',
             'test_is_dir_valid_fail',
             'test_ng_dest_ok',
             'test_ng_dest_fail',
             'test_ng_read_ok',
             'test_ng_read_fail',
             'test_ng_filepath_ok',
             'test_extract_yaml_ok',
             'test_extract_yaml_fail',
             'test_extract_yaml_tags_ok',
             'test_extract_yaml_tags_fail',
             'test_extract_yaml_date_ok',
             'test_extract_yaml_date_fail',
             'test_update_tags_ok',
             'test_update_tags_fail',
             'test_read_ok',
             'test_read_fail']

    return unittest.TestSuite(map(TestNg, tests))


if __name__ == "__main__":
    suite()
    unittest.main()


# vim: ff=unix:ts=4:sw=4:tw=78:noai:expandtab
