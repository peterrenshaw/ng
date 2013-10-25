#!/usr/bin/env python
# ~*~ encoding: utf-8 ~*~


#---
# copy: copyright (C) 2013 Peter Renshaw
#---


import os
import unittest


import hack_page2


class TestPage(unittest.TestCase):
    def setUp(self):
        self.is_index = False  # is current page an index page (ie:
                               # yyyy/mmm/index.html or just ord
                               # page?
        self.p = hack_page2.Page(self.is_index)
    def tearDown(self):
        self.p = None

    # init
    def test_page_init(self):
        self.assertTrue(self.p)
    # header
    def test_header_ok(self):
        self.assertTrue(self.p.header("content"))
    def test_header_fail(self):
        self.assertFalse(self.p.header(""))
    # body
    def test_body_ok(self):
        self.assertTrue(self.p.body("title","abstract","content","template"))
    def test_body_none_ok(self):
        self.assertFalse(self.p.body(title="",abstract="",content="",template=""))
    def test_body_no_abstract_fail(self):
        self.assertFalse(self.p.body(title="title",abstract="",content="content",template="template"))
    def test_body_no_content_fail(self):
        self.assertFalse(self.p.body(title="title",abstract="abstract",content="",template=""))
    def test_body_no_title_fail(self):
        self.assertFalse(self.p.body(title="",abstract="abstract",content="content",template=""))
    def test_body_fail(self):
        self.assertFalse(self.p.body("","","",""))
    # filename
    def test_filename_ok(self):
        #self.assertTrue(self.p.filename(os.curdir, 'filename','html'))
        pass
    def test_filename_path_fail(self):
        #self.assertFalse(self.p.filename('c:\\tmp', 'filename','htm'))
        pass
    def test_filename_filename_fail(self):
        #self.assertFalse(self.p.filename(os.curdir, '','htm'))
        pass
    def test_filename_est_fail(self):
        #self.assertFalse(self.p.filename(os.curdir, 'filename','XHTML'))
        pass
    # footer
    def test_footer_ok(self):
        self.assertTrue(self.p.footer("content"))
    def test_footer_fail(self):
        self.assertFalse(self.p.footer(""))
    # metadata
    def test_metadata_ok(self):
        self.assertTrue(self.p.metadata(tags=['this','that','them','us']))
    def test_metadata_fail(self):
        #self.assertFalse(self.p.metadata(foo="this isn't a valid key"))
        pass
    def test_metadata_update_data_ok(self):
        """set meta_data['year'] to 2012, update to 2013 & compare, T"""
        update_year = "2013"
        self.assertTrue(self.p.metadata(tags=['this','that','them','us'], 
                                        year="2012"))
        self.assertTrue(self.p.metadata(year=update_year))
        #self.assertEqual(update_year, self.p.meta_data['year'])
    def test_metadata_update_data_fail(self):
        """blank update shouldn't update existing data"""
        #update_year = ""
        #self.assertTrue(self.p.metadata(tags=['this','that','them','us'], 
        #                                year="2012"))
        #print("%s %s" % (update_year, self.p.meta_data['year']))
        #self.assertFalse(self.p.metadata(year=update_year))
        #print("%s %s" % (update_year, self.p.meta_data['year']))
        #self.assertNotEqual(update_year, self.p.meta_data['year'])
        pass
    # get
    def test_get_ok(self):
        #self.assertFalse(self.p.get('meta','is_index'))
        pass
    def test_get_empty_fail(self):
        #self.assertFalse(self.p.get("",""))
        pass
    def test_get_body_ok(self):
        #self.p.body('title','abstract','content','template')
        #self.assertTrue(self.p.get_body('title'))
        pass
    def test_get_meta_ok(self):
        #self.p.metadata(tags=['foo','bar','foobar'])
        #self.assertTrue(self.p.get_meta('tags'))
        pass
    def test_get_file_ok(self):
        """remember correct extension enforced"""
        #self.assertTrue(self.p.filename(path=os.curdir, name='foo',ext='html'))
        pass

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
             'test_filename_est_fail',
             'test_metadata_ok',
             'test_metadata_fail',
             'test_metadata_update_data_ok',
             'test_get_ok',
             'test_get_empty_fail',
             'test_get_body_ok',
             'test_get_meta_ok',
             'test_get_file_ok']

    return unittest.TestSuite(map(TestPage, tests))


if __name__ == "__main__":
    suite()
    unittest.main()


# vim: ff=unix:ts=4:sw=4:tw=78:noai:expandtab
