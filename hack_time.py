#!/usr/bin/env python
# ~*~ encoding: utf-8 ~*~

import time
import datetime
from datetime import date


# birthtime = datetime.datetime(1973, 01, 18, 3, 45, 50)   # 1973-01-18 03:45:50
#  YYYY-MM-DDTHH:MM:SS
# <http://docs.python.org/2/library/datetime.html#datetime.datetime.isoformat>
# <http://pleac.sourceforge.net/pleac_python/datesandtimes.html>
# <http://docs.python.org/2/library/datetime.html>

st = "2013-10-10T14:08:00"
# dt_iso_valid: check  if "YYYY-MM-DDTHH:MM:SS"
def dt_iso_8601_valid(dts):
    """break down ISO format string"""
    if len("YYYY-MM-DDTHH:MM:SS") == len(dts):
        if dts[4] == "-":
            if dts[7] == "-":
                if dts[10] == "T":
                    if dts[13] == ":":
                        if dts[16] == ":":
                             return True
    return False
# dt_iso_crack: crack "YYYY-MM-DDTHH:MM:SS"
def dt_iso_8601_crack(dts):
    """break into bits, assumes valid"""
    year = int(dts[0:4])
    month = int(dts[5:7])
    day = int(dts[8:10])
    hh = int(dts[14:16])
    mm = int(dts[17:19])
    return year, month, day, hh, mm
def dt_str_8601_to_epoch(year, month, day, hour, minute):
    """convert into epoch, assumes valid"""
    t = datetime.datetime(year, month, day, hour, minute)
    return time.mktime(t.timetuple())
def dt_str_8601_to_date(year, month, day):
    return datetime.date(year, month, day)
def dt_iso_8601_utc():
    """return YYYY-MM-DDTHH:MM:SS"""
    t = datetime.datetime.utcnow()
    return time.mktime(t.timetuple())
def dt_iso_8601_utc_offset():
    t = datetime.datetime.now()
    return time.mktime(t.timetuple())

def main():
    if dt_iso_8601_valid(st):
        year, month, day, hh, mm = dt_iso_8601_crack(st)
        print(year, month, day, hh, mm)

        epoch = dt_str_8601_to_epoch(year, month, day, hh, mm)
        print(epoch)

        dt = dt_str_8601_to_date(year, month, day)
        print(dt)

        euct = dt_iso_8601_utc()
        print(euct)

        eutco = dt_iso_8601_utc_offset()
        print(eutco)
#---
# main app entry point
#--- 
if __name__ == '__main__':
    main()


# vim: ff=unix:ts=4:sw=4:tw=78:noai:expandtab
