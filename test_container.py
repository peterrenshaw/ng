#!/usr/bin/env python
# ~*~ encoding: utf-8 ~*~


#---
# copy: copyright (C) 2013 Peter Renshaw
#---


import os
import unittest

# TODO change this when rebuild 
import hack_page2
from hack_page2 import dt_ymdhm2_epoch


class TestContainer(unittest.TestCase):
    def setUp(self):
        self.c = hack_page2.Container()
    def tearDown(self):
        self.c = None

    def test_cont_init(self):
        """obj instantiated?"""
        self.assertTrue(self.c)
    def test_cont_add_ok(self):
        """add is valid, return T else F"""
        self.c.add(epoch=dt_ymdhm2_epoch(year=2013,month=10,day=1,hour=0,minute=0),
           title='Hello world #1',url='http://192.168.0.1',year=2013,month=4, 
           day=1, hour=0,minute=0)
        self.assertTrue(self.c.all())
    def test_cont_add_fail(self):
        """nothing to add, should be F"""
        self.assertFalse(self.c.add())
    def test_cont_clear_ok(self):
        """full list, clear returns nothing"""
        self.c.add(epoch=dt_ymdhm2_epoch(year=2013,month=10,day=1,hour=0,minute=0),
           title='Hello world #1',url='http://192.168.0.1',year=2013,month=4, 
           day=1, hour=0,minute=0)
        self.assertFalse(self.c.clear())
    def test_cont_all_ok(self):
        """add N, return should return N items in list"""
        # add 2
        self.c.add(epoch=dt_ymdhm2_epoch(year=2013,month=10,day=1,hour=0,minute=0),
           title='Hello world #1',url='http://192.168.0.1',year=2013,month=4, 
           day=1, hour=0,minute=0)
        self.c.add(epoch=dt_ymdhm2_epoch(year=2013,month=10,day=23,hour=0,minute=0),
           title='The latest post',url='http://foo.com/bar/foobar',year=2013,
           month=10,day=23, hour=0, minute=0)
        length = len(self.c.all())
        self.assertEqual(length, 2)
        self.assertTrue(self.c.all())
    def test_cont_all_empty_ok(self):
        """empty list, should be lenght zero"""
        length = len(self.c.all())
        self.assertEqual(length, 0)
    def test_cont_sort_order_ok(self):
        """sorting on numbers, order should be as expected"""
        self.c.add(epoch=dt_ymdhm2_epoch(year=2011,month=11,day=11,hour=11,minute=11),
           title='First post',url='http://foo.com/bar',year=2011,month=11,
           day=11, hour=11, minute=11)
        self.c.add(epoch=dt_ymdhm2_epoch(year=2001,month=1,day=1,hour=1,minute=1),
           title='Hello world #1',url='http://192.168.0.1',year=2001,month=1, 
           day=1, hour=1,minute=1)
        self.c.add(epoch=dt_ymdhm2_epoch(year=2010,month=10,day=10,hour=10,minute=10),
           title='The latest post',url='http://foo.com/bar/foobar',year=2010,
           month=10,day=10, hour=10, minute=10)
        self.c.add(epoch=dt_ymdhm2_epoch(year=2012,month=12,day=12,hour=12,minute=12),
           title='Hello world #2',url='http://foo.com',year=2012,month=12,
           day=12, hour=12, minute=12)
        data = self.c.sort('epoch')
        year =   (data[0]['year'] > data[3]['year'])
        month =  (data[0]['month'] > data[3]['month'])
        day =    (data[0]['day'] > data[3]['day'])
        hour =   (data[0]['hour'] > data[3]['hour'])
        minute = (data[0]['minute'] > data[3]['minute'])
        epoch =  (data[0]['epoch'] > data[3]['epoch'])

        self.assertTrue(epoch and year and month and day and hour and minute)
    def test_cont_sort_order_reverse_ok(self):
        """sorting on numbers, order should be as expected"""
        self.c.add(epoch=dt_ymdhm2_epoch(year=2011,month=11,day=11,hour=11,minute=11),
           title='First post',url='http://foo.com/bar',year=2011,month=11,
           day=11, hour=11, minute=11)
        self.c.add(epoch=dt_ymdhm2_epoch(year=2001,month=1,day=1,hour=1,minute=1),
           title='Hello world #1',url='http://192.168.0.1',year=2001,month=1, 
           day=1, hour=1,minute=1)
        self.c.add(epoch=dt_ymdhm2_epoch(year=2010,month=10,day=10,hour=10,minute=10),
           title='The latest post',url='http://foo.com/bar/foobar',year=2010,
           month=10,day=10, hour=10, minute=10)
        self.c.add(epoch=dt_ymdhm2_epoch(year=2012,month=12,day=12,hour=12,minute=12),
           title='Hello world #2',url='http://foo.com',year=2012,month=12,
           day=12, hour=12, minute=12)
        data = self.c.sort('epoch', order=False)
        year =   (data[0]['year'] < data[3]['year'])
        month =  (data[0]['month'] < data[3]['month'])
        day =    (data[0]['day'] < data[3]['day'])
        hour =   (data[0]['hour'] < data[3]['hour'])
        minute = (data[0]['minute'] < data[3]['minute'])
        epoch =  (data[0]['epoch'] < data[3]['epoch'])

        self.assertTrue(epoch and year and month and day and hour and minute)
    def test_cont_sort_term_fail(self):
        """sort fails?"""
        self.c.add(epoch=dt_ymdhm2_epoch(year=2010,month=10,day=10,hour=10,minute=10),
           title='The latest post',url='http://foo.com/bar/foobar',year=2010,
           month=10,day=10, hour=10, minute=10)
        self.c.add(epoch=dt_ymdhm2_epoch(year=2012,month=12,day=12,hour=12,minute=12),
           title='Hello world #2',url='http://foo.com',year=2012,month=12,
           day=12, hour=12, minute=12)
        data = self.c.sort('epoch')
        length = len(data)
        self.assertTrue(length == 2)
    def test_cont_sort_term_fail(self):
        """sort fails?"""
        self.c.add(epoch=dt_ymdhm2_epoch(year=2010,month=10,day=10,hour=10,minute=10),
           title='The latest post',url='http://foo.com/bar/foobar',year=2010,
           month=10,day=10, hour=10, minute=10)
        self.c.add(epoch=dt_ymdhm2_epoch(year=2012,month=12,day=12,hour=12,minute=12),
           title='Hello world #2',url='http://foo.com',year=2012,month=12,
           day=12, hour=12, minute=12)
        data = self.c.sort('FOO')
        self.assertFalse(data)
    def test_cont_sort_no_term_fail(self):
        """sort fails?"""
        self.c.add(epoch=dt_ymdhm2_epoch(year=2010,month=10,day=10,hour=10,minute=10),
           title='The latest post',url='http://foo.com/bar/foobar',year=2010,
           month=10,day=10, hour=10, minute=10)
        self.c.add(epoch=dt_ymdhm2_epoch(year=2012,month=12,day=12,hour=12,minute=12),
           title='Hello world #2',url='http://foo.com',year=2012,month=12,
           day=12, hour=12, minute=12)
        data = self.c.sort('')
        self.assertFalse(data)


#---
# suite: allows all tests run here to be run externally at 'test_all.py'
#---
def suite():
    """tests added to run in 'test_all.py'"""
    tests = ['test_cont_init',
             'test_cont_add_ok',
             'test_cont_add_fail',
             'test_cont_clear_ok',
             'test_cont_all_ok',
             'test_cont_all_empty_ok',
             'test_cont_sort_order_ok',
             'test_cont_sort_order_reverse_ok',
             'test_cont_sort_term_fail',
             'test_cont_sort_no_term_fail'
            ]

    return unittest.TestSuite(map(TestContainer, tests))


if __name__ == "__main__":
    suite()
    unittest.main()


# vim: ff=unix:ts=4:sw=4:tw=78:noai:expandtab
