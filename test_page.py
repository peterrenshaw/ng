#!/usr/bin/env python
# ~*~ encoding: utf-8 ~*~


#---
# copy: copyright (C) 2013 Peter Renshaw
#---


import os
import unittest


import hack_page


class TestPage(unittest.TestCase):
    def setUp(self):
        self.p = hack_page.Page()
    def tearDown(self):
        self.p = None

    # init
    def test_page_init(self):
        self.assertTrue(self.p)
    # adding data
    def test_header_ok(self):
        self.assertTrue(self.p.header("content"))
    def test_header_fail(self):
        self.assertFalse(self.p.header(""))
    def test_body_ok(self):
        self.assertTrue(self.p.body("title","abstract","content"))
    def test_body_none_ok(self):
        self.assertFalse(self.p.body(title="",abstract="",content=""))
    def test_body_no_abstract_fail(self):
        self.assertFalse(self.p.body(title="title",abstract="",content="content"))
    def test_body_no_content_fail(self):
        self.assertFalse(self.p.body(title="title",abstract="abstract",content=""))
    def test_body_no_title_fail(self):
        self.assertFalse(self.p.body(title="",abstract="abstract",content="content"))
    def test_body_fail(self):
        self.assertFalse(self.p.body("","",""))
    def test_filename_ok(self):
        self.assertTrue(self.p.filename(os.curdir, 'filename','html'))
    def test_filename_path_fail(self):
        self.assertFalse(self.p.filename('c:\\tmp', 'filename','htm'))
    def test_filename_filename_fail(self):
        self.assertFalse(self.p.filename(os.curdir, '','htm'))
    def test_filename_est_fail(self):
        self.assertFalse(self.p.filename(os.curdir, 'filename','XHTML'))
    def test_footer_ok(self):
        self.assertTrue(self.p.footer("content"))
    def test_footer_fail(self):
        self.assertFalse(self.p.footer(""))
    


#---
# suite: allows all tests run here to be run externally at 'test_all.py'
#---
def suite():
    """tests added to run in 'test_all.py'"""
    tests = ['test_page_init',
             'test_header_ok',
             'test_header_fail',
             'test_body_ok',
             'test_body_none_ok',
             'test_body_no_title_fail',
             'test_body_no_abstract_fail',
             'test_body_no_content_fail',
             'test_body_fail',
             'test_footer_ok',
             'test_footer_fail',
             'test_filename_ok',
             'test_filename_path_fail',
             'test_filename_filename_fail',
             'test_filename_est_fail']

    return unittest.TestSuite(map(TestPage, tests))


if __name__ == "__main__":
    suite()
    unittest.main()


# vim: ff=unix:ts=4:sw=4:tw=78:noai:expandtab
