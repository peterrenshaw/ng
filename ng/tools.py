#!/usr/bin/env python
# ~*~ encoding: utf-8 ~*~


#===
# name: tools.py
# date: 2013OCT09
# prog: pr
# desc: quick hack for a not so nextgen 
#       static html site generator
#===


import os
import sys
import time
import shutil
import os.path
import datetime


# --- time tools ---
#

#---
# dt_is_valid_input: pass in y/m/d/h:m checks valid, spits out T/F
#                    optional: min_year refers to epoch start year
#                    no test for epoch start month or day.
#---
def dt_is_valid_input(year, month, day, hour, minute, min_year=1970):
    """check for sane inputs, return T or f"""
    #print("1 year=%s month=%s day=%s hour=%s minute=%s" % 
    #                         (year, month, day, hour, minute))
    if year >= min_year:
        if month >= 1 and month <= 12:
            if day >= 1 and day <= 31:
                if hour >= 0 and hour <= 24:
                    if minute >= 0 and minute <= 59:
                        return True
    return False
#---
# dt_ymdhm2_epoch: pass in y/m/d/h:m spits out epoch
#---
def dt_ymdhm2_epoch(year, month, day, hour, minute): # TODO add optional seconds
    """return datetime in epoch format defined by y,m (mm format),d,h,m"""
    if dt_is_valid_input(year, month, day, hour, minute):
        t = datetime.datetime(year, month, day, hour, minute)
        return time.mktime(t.timetuple())
    else:
        return False
#---
# dt_ymdhm2_strf: pass in y/m/d/h:m spits out formatted date as string
#                 optional: strf_format cf: formatting of date using strformat
#                 is_upper: upper or lower case display?
#---
def dt_ymdhm2_strf(year, month, day, hour, minute, 
                   strf_format="%A, %d %B %Y %H:%M",is_upper=False):
    """return datetime as strf formattd time defined by y,m,d,h,m"""
    if dt_is_valid_input(year, month, day, hour, minute):
        dt = datetime.datetime(year,month,day,hour,minute).strftime(strf_format)
        if is_upper:
            return dt.upper()
        else:
            return dt
    else:
        return False
    
#--- KILL ---
#---
# dt_epoch_utc: epoch, utc
#---
def dt_epoch_utc():
    """return datetime in UTC epoch format"""
    t = datetime.datetime.utcnow()
    return time.mktime(t.timetuple())
#---
# dt_datetime_strf: format return using strf strings
#---
def dt_datetime_strf(strf_format, is_upper=False):
    """datetime formatted using STRF string format"""
    dt = datetime.datetime.now().strftime(strf_format)
    if is_upper: dt = dt.upper()
    return dt
#--- KILL ---

#===
# name: DateISO8601
# date: 2013OCT09
# prog: pr:
# desc: naive time tool for iso-8601
#
# cf:   <http://docs.python.org/2/library/datetime.html>
# eg:   2013-10-10T14:08:00
#       YYYY-MM-DDTHH:MM:SS
# nb:   no now, epoch, utc 
#       all datetime from str
#===
class DateIso8601:
    def __init__(self, str_iso_8601="", dt=datetime):
        """initialise variables and set up structures"""
        self.iso = str_iso_8601  # YYYY-MM-DDTHH:MM:SS
        self.dt = datetime       # passed in date object
        self.is_valid = False    # is str_iso_8601 valid format?
        
        self.epoch = 0   # int because we use epoch to 
        self.year = 0
        self.month = 0
        self.month_mm = 0
        self.month_mmm = ""
        self.day = 0
        self.hour = 0
        self.minute = 0
        self.seconds = 0

        self.mmm = ['JAN','FEB','MAR','APR', \
                    'MAY','JUN','JUL','AUG', \
                    'SEP','OCT','NOV','DEC']

        self.iso_8601 = "YYYY-MM-DDTHH:MM:SS"
        self.iso_8601_strf = "%Y-%m-%dT%H:%M:%S"
        self.iso_8601_date_strf = "%Y-%m-%d"

    def validate(self, str_iso_8601=""):
        """validate string format to ISO8601 standard"""
        # test for current or new 
        if str_iso_8601:
            iso = str_iso_8601
        else:
            iso = self.iso
        if len(self.iso_8601) == len(iso):
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
        else:
            iso = self.iso

        self.validate(iso)   # don't assume valid, re-validate
        if self.is_valid:
            self.iso = iso
               
            #  YYYY-MM-DDTHH:MM:SS
            #  0123456789012345678
            #  1234567890123456789
            #  2013-10-10T14:08:00
            self.year =     int(self.iso[0:4])
            self.month_mm = int(self.iso[5:7])
            self.month = self.month_mm
            self.day =      int(self.iso[8:10])

            # convert mm to mmm
            self.month_mmm = ""
            count = 1
            for dd in self.mmm:
                if count == int(self.month_mm):
                    # one off error?
                    self.month_mmm = self.mmm[count-1]
                    break
                count += 1

            self.hour = int(self.iso[11:13])
            self.minute = int(self.iso[14:16])

            # epoch from given date
            self.epoch = float(self.build_epoch(self.year, 
                                              self.month, 
                                              self.day, 
                                              self.hour,
                                              self.minute))

            return (self.epoch, self.year, self.month, self.month_mm,
                    self.month_mmm, self.day, self.hour, self.minute)
        else: 
            return False
    def build_epoch(self, year, month_mm, day, hour, minute):
        """return ISO6601 as epoch"""
        if dt_is_valid_input(year, month_mm, day, hour, minute):
            t = dt_ymdhm2_epoch(year, month_mm, day, hour, minute)
            self.epoch = t
            return self.epoch
        else:
            return False
    def date(self):
        """returns ISO6601 as YYYY-MM-DD"""
        if self.is_valid:
            self.dt_date = datetime.date(self.year, self.month, self.day)
            date = self.dt_date.strftime(self.iso_8601_date_strf)
            return date
        else:
            return False
    def now(self):
        """return datetime UTC now as ISO6601"""
        # So if you don't explicitly state the time, this call will be UTC
        # for now - because local time is complex
        # "YYYY-MM-DDTHH:MM:SS"
        # <http://cpan.uwinnipeg.ca/htdocs/Time-Piece-ISO/Time/Piece/ISO.html>
        # TODO gmt or local time, ability to specify
        dt = datetime.datetime.utcnow().strftime(self.iso_8601_strf)
        if self.validate(dt):
            return dt
        else:
            return False
#
# --- end time tools ---


# --- string tools ---
def remove_char(value, replacement=""):
    """remove the crap"""
    if value:
        crap = ["'","!","@","#","$","%","^","*",
                "(",")","+","[","]","{","}","|",
                "\\",":",",",".","/"]
        for char in crap:
            value = value.replace(char, replacement)
        return value
    return False
# --- end string tools ---

# --- start path tools ---
def build_respath(path, bw="..", is_web=True):
    """
    build the resource path back to root from existing
    path and return resource path data or F
    """
    # check for os.path.altsep in path & die
    # as it gives unpredictable result
    if not path.count(os.path.altsep) > 0:
        if path: 
            if is_web:
                sep = "/"
            else: 
                sep = os.path.sep

            resdata = ""
            # because counting b/w path
            count = path.count(os.path.sep) + 1
            for c in range(0, count):
                resdata = "%s%s%s" % (resdata, bw, sep)
            if is_web:
                if count > 1:
                    resdata = resdata[:-1]
            return resdata
    return False
# --- end path tools ---


# main entry point
def main():
    pass

#---
# main app entry point
#--- 
if __name__ == '__main__':
    main()


# vim: ff=unix:ts=4:sw=4:tw=78:noai:expandtab
