#!/usr/bin/env python
# ~*~ encoding: utf-8 ~*~

#---
# copy: copyright (C) 2013 Peter Renshaw
#---


import unittest


import test_ng 
import test_date
import test_page
import test_container


#---
# suite: allows all tests run here to be run externally at 'test_all.py'
#---
def main():
    """tests added to run in 'test_all.py'"""
    # add all new test suites per test module here
    suite_date = test_date.suite()
    suite_ng = test_ng.suite()
    suite_page = test_page.suite()
    suite_container = test_container.suite()

    # add the suite to be tested here
    alltests = unittest.TestSuite((suite_date,
                                   suite_ng,
                                   suite_page,
                                   suite_container))

    # run the suite
    runner = unittest.TextTestRunner()
    runner.run(alltests)


if __name__ == "__main__":
    main()


# vim: ff=unix:ts=4:sw=4:tw=78:noai:expandtab
