#!/usr/bin/env python
# ~*~ encoding: utf-8 ~*~

import time
import datetime
from datetime import date


class Date8601:
    def __init__(self, str_iso_8601="", dt=datetime):
        self.iso = str_iso_8601  # YYYY-MM-DDTHH:MM:SS
        self.dt = datetime       # passed in date object
        self.is_valid = False    # is str_iso_8601 valid format?
        
        self.year = 0
        self.month = 0
        self.month_mm = 0
        self.month_mmm = ""
        self.day = 0
        self.hour = 0
        self.minute = 0
        self.seconds = 0
        self.mmm = ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']
    def validate(self, str_iso_8601=""):
        """validate string format to ISO8601 standard"""
        # test for current or new 
        if str_iso_8601:
            iso = str_iso_8601
        else:
            iso = self.iso
        if len("YYYY-MM-DDTHH:MM:SS") == len(iso):
            if iso[4] == "-":
                if iso[7] == "-":
                    if iso[10] == "T":
                        if iso[13] == ":":
                            if iso[16] == ":":
                                 self.iso = iso        # update 
                                 self.is_valid = True
                                 return self.is_valid
        self.is_valid = False
        return self.is_valid
    def crack(self, str_iso_8601=""):
        """break apart string format ISO8601 into time"""
        # test for supplied or current
        if str_iso_8601: 
            iso = str_iso_8601
            self.validate(iso)
        else:
            iso = self.iso
        if self.is_valid:
            self.iso = iso
            # "2013-10-10T14:08:00"
            self.year = int(self.iso[0:4])
            self.month = int(self.iso[5:7])
            self.month_mm = int(self.iso[5:7])
            count = 1
            for dd in self.mmm:
                if count == self.month_mm:
                    self.month_mmm = self.mmm[count]
                    break
                count += 1
            self.day = int(self.iso[8:10])
            self.hour = int(self.iso[14:16])
            self.minute = int(self.iso[17:19])

            return self.year, self.month, \
                   self.day, self.hour, self.minute
        else: 
            return False
    def epoch(self):
        """return ISO6601 as epoch"""
        if self.is_valid:
            t = datetime.datetime(self.year, self.month, self.day, 
                                  self.hour, self.minute)
            self.epoch = time.mktime(t.timetuple())
            return self.epoch
        else:
            return False
    def date(self):
        """returns ISO6601 as YYYY-MM-DD"""
        if self.is_valid:
            self.dt_date = datetime.date(self.year, self.month, self.day)
            return self.dt_date
        else:
            return False

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
#               to     2013 10 10 8 0
def dt_iso_8601_crack(dts):
    """break into bits, assumes valid"""
    year = int(dts[0:4])
    month = int(dts[5:7])
    day = int(dts[8:10])
    hh = int(dts[14:16])
    mm = int(dts[17:19])
    return year, month, day, hh, mm
# dt_str_8601_to_epoch: generates for eg: 1381352400.0
def dt_str_8601_to_epoch(year, month, day, hour, minute):
    """convert into epoch, assumes valid"""
    t = datetime.datetime(year, month, day, hour, minute)
    return time.mktime(t.timetuple())
# dt_str_8601_to_date: generates for eg: 2013-10-10
def dt_str_8601_to_date(year, month, day):
    return datetime.date(year, month, day)
# dt_iso_8601_utc: generates utc: 1381339265.0
def dt_iso_8601_utc():
    """return YYYY-MM-DDTHH:MM:SS"""
    t = datetime.datetime.utcnow()
    return time.mktime(t.timetuple())
# dt_iso_8601_utc_offset: generates utc+offset 138137865.0
def dt_iso_8601_utc_offset():
    t = datetime.datetime.now()
    return time.mktime(t.timetuple())

def main():
    print("created")
    d = Date8601(st)
    if d.validate():
        print("valid")
        if d.crack():
            print("cracked")
            epoch = d.epoch()
            date = d.date()
            print(epoch)
            print(date)
            print(d.year)
            print(d.month)
            print(d.month_mm)
            print(d.month_mmm)
            print(d.day)
            print(d.hour)
            print(d.minute)
    else:
        print("invalid date <%s>" % st)
    d = None
    

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
