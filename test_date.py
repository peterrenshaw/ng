#!/usr/bin/env python
# ~*~ encoding: utf-8 ~*~


#---
# copy: copyright (C) 2013 Peter Renshaw
#---


import os.path
import unittest


import ng


class TestDate(unittest.TestCase):
    def setUp(self):
        self.d = ng.DateIso8601()
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
        (year, month, month_mm, month_mmm, day, hour, minute) = self.d.crack()
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
        (year, month, month_mm, month_mmm, day, hour, minute) = self.d.crack()
        self.assertEqual(year, 2013)
        self.assertEqual(month, 10)
        self.assertEqual(day, 10)
        self.assertEqual(self.d.date(),'2013-10-10')

    # process
#---
# suite: allows all tests run here to be run externally at 'test_all.py'
#---
def suite():
    """tests added to run in 'test_all.py'"""
    tests = ['test_date_init',
             'test_date_validate_ok',
             'test_date_validate_false',
             'test_crack_ok',
             'test_date_ok]

    return unittest.TestSuite(map(TestDate, tests))


if __name__ == "__main__":
    suite()
    unittest.main()


# vim: ff=unix:ts=4:sw=4:tw=78:noai:expandtab