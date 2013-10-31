#!/usr/bin/env python
# ~*~ encoding: utf-8 ~*~


#---
# copy: copyright (C) 2013 Peter Renshaw
#---


import os.path
import unittest


import ng.tools


class TestDate(unittest.TestCase):
    def setUp(self):
        self.d = ng.tools.DateIso8601()
        self.iso_valid = "2013-10-10T14:08:00"
        self.iso_invalid = "2013-10 10 14:08 00"
    def tearDown(self):
        self.d = None
        self.iso_valid = None
        self.iso_invalid = None

    # init
    def test_date_init(self):
        """init"""
        self.assertTrue(self.d)
    def test_date_validate_ok(self):
        """validation true"""
        self.assertTrue(self.d.validate(self.iso_valid))
    def test_date_validate_false(self):
        """validation fails"""
        self.assertFalse(self.d.validate(self.iso_invalid))
    def test_crack_ok(self):
        """break iso down, pass"""
        self.d.validate(self.iso_valid)
        (epoch, year, month, month_mm, month_mmm, day, hour, minute) = self.d.crack()
        self.assertEqual(year, 2013)
        self.assertEqual(month, 10)
        self.assertEqual(month_mm, 10)
        self.assertEqual(month_mmm, 'OCT')
        self.assertEqual(day, 10)
        self.assertEqual(hour, 14)
        self.assertEqual(minute, 8)
    def test_date_ok(self):
        """extract iso date, ok"""
        status = self.d.validate(self.iso_valid)
        self.assertTrue(status)
        (epoch, year, month, month_mm, month_mmm, day, hour, minute) = self.d.crack()
        self.assertEqual(year, 2013)
        self.assertEqual(month, 10)
        self.assertEqual(day, 10)
        self.assertEqual(self.d.date(),'2013-10-10')
    def test_date_fail(self):
        """test date fails on invalid iso format"""
        self.d.validate(self.iso_invalid)
        self.d.crack()
        self.assertFalse(self.d.date())
    def test_epoch_ok(self):
        """return epoch from ISO8601 in string format"""
        status = self.d.validate(self.iso_valid)
        self.assertTrue(status)
    def test_epoch_fail(self):
        """return F from epoch with invalid ISO8601 in str fmt"""
        status = self.d.validate(self.iso_invalid)
        self.assertFalse(status)


#---
# suite: allows all tests run here to be run externally at 'test_all.py'
#---
def suite():
    """tests added to run in 'test_all.py'"""
    tests = ['test_date_init',
             'test_date_validate_ok',
             'test_date_validate_false',
             'test_crack_ok',
             'test_date_ok',
             'test_date_fail',
             'test_epoch_ok',
             'test_epoch_fail']

    return unittest.TestSuite(map(TestDate, tests))


if __name__ == "__main__":
    suite()
    unittest.main()


# vim: ff=unix:ts=4:sw=4:tw=78:noai:expandtab
