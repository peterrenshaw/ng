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
        self.source_dir = os.getcwd()  # assumption: has valid files
        self.source_dir_fail = os.path.join(self.source_dir, 'foo')
        self.yyyy = "2013"
        self.mm = "10"
        self.mmm = "OCT"
        self.dd = "12"
    def tearDown(self):
        path = self.n.path_yyyy(self.yyyy)
        self.n.remove_directory(path)
        self.yyyy = None
        self.n = None
        self.soruce_dir = None
        self.source_dir_fail = None
        self.mm = None
        self.mmm = None
        self.dd = None


    # init
    def test_ng_init(self):
        self.assertTrue(self.n)

    # directory
    def test_is_dir_valid_ok(self):
        self.assertTrue(self.n.is_dir_valid(self.source_dir))
    def test_is_dir_valid_fail(self):
        self.assertFalse(self.n.is_dir_valid(self.source_dir_fail))
    def test_ng_dest_ok(self):
        self.assertTrue(self.n.destination(self.source_dir))
    def test_ng_dest_fail(self):
        self.assertFalse(self.n.destination(self.source_dir_fail))
    def test_create_dir_yyyy_ok(self):
        path = self.n.path_yyyy(self.yyyy)
        self.assertTrue(self.n.create_directory(path))
    def test_create_dir_yyyy_fail(self):
        pass
    def test_create_dir_yyyy_mm_ok(self):
        pass
    def test_create_dir_yyyy_mm_fail(self):
        pass
    def test_create_dir_yyyy_mm_dd_ok(self):
        pass
    def test_create_dir_yyyy_mm_dd_fail(self):
        pass
    def test_create_dir_yyyy_mmm_ok(self):
        pass
    def test_create_dir_yyyy_mmm_fail(self):
        pass
    def test_create_dir_yyyy_mmm_dd_ok(self):
        pass
    def test_create_dir_yyyy_mmm_dd_fail(self):
        pass

    # read
    def test_ng_read_ok(self):
        self.assertTrue(self.n.read(self.source_dir))
    def test_ng_read_fail(self):
        self.assertFalse(self.n.read(""))

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
        self.assertTrue(self.n.read(self.source_dir))
    def test_read_fail(self):
        self.assertFalse(self.n.read(""))

    # process
#---
# suite: allows all tests run here to be run externally at 'test_all.py'
#---
def suite():
    """tests added to run in 'test_all.py'"""
    tests = ['test_ng_init',
             'test_is_dir_valid_ok',
             'test_is_dir_valid_fail',
             'test_ng_dest_ok',
             'test_ng_dest_fail',
             'test_ng_read_ok',
             'test_ng_read_fail',
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
