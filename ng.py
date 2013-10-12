#!/usr/bin/env python
# ~*~ encoding: utf-8 ~*~


#===
# name: ng.py
# date: 2013OCT09
# prog: pr
# desc: quick hack for a not so nextgen 
#       static html site generator
# use : ng.py -f <source> -d <dest>
#===


import os
import sys
import glob
import time
import os.path
import datetime
from optparse import OptionParser


# --- time tools start---
#
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

            #  0123456789012345678
            #  2013-10-10T14:08:00
            self.year = int(self.iso[0:4])
            self.day = int(self.iso[5:7])
            self.month = int(self.iso[8:10])
            self.month_mm = int(self.iso[5:7])

            # convert mm to mmm
            self.month_mmm = ""
            count = 1
            for dd in self.mmm:
                if count == int(self.month_mm):
                    #print(count, dd, self.mmm[count-1])
                    self.month_mmm = self.mmm[count-1] # one off error?
                    break
                count += 1

            self.hour = int(self.iso[11:13])
            self.minute = int(self.iso[14:16])

            return self.year, self.month, self.month_mm, \
                   self.month_mmm, self.day, self.hour, \
                   self.minute
        else: 
            return False
    def epoch(self):
        """return ISO6601 as epoch"""
        self.crack()
        if self.is_valid:
            t = datetime.datetime(self.year, self.month, self.day, self.hour, self.minute)
            self.epoch = time.mktime(t.timetuple())
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


#===
# name: Nextgen
# date: 2013OCT09
# prog: pr
# desc: hack an old, nextgeneration static blog
#       engine in 8 hrs (no)
# usge: 
#            ng = Nextgen()
#            ng.source(<source directory>)
#            ng.destination(<destination directory>)
#            ng.process()
#===
class Nextgen:
    def __init__(self, d8601=DateIso8601()):
        """inject Date object, init variables"""
        self.date8601 = d8601
        self.source_dir = ""
        self.dest_dir = ""
        self.ext = ["md","markdown","txt"]
        self.filepath = []
        self.post = []
        self.is_raw = True
        self.yaml = []
    # directories
    def is_dir_valid(self, file_dir):
        """valid directory or F"""
        if file_dir:
            if os.path.isdir(file_dir):
                    return file_dir
        return False
    def destination(self, file_dir=""):
        """valid destination directory or F"""
        fdp = self.is_dir_valid(file_dir)
        if fdp: 
            self.dest_dir = fdp
            return True
        else:
            return False
    # filepaths
    def read_file_content(self, filename):
        """read file contents or F"""
        if os.path.isfile(filename):
           data = ""
           f = None
           try: 
               with open(filename) as f:
                   data = f.read()
               f.close()
               return data
           except:
               data = ""
               if f: f.close()
        return False
    def read_file_name(self, dir_path, ext):
        """read all filepaths given ext and directory path"""
        glob_ext = "*.%s" % ext
        gfp = os.path.join(dir_path, glob_ext)
        fpn = [os.path.realpath(f) for f in glob.glob(gfp)]
        return fpn
    def read_file_names(self, dir_path):
        rf = []
        for extension in self.ext:
            read_file = self.read_file_name(dir_path, extension)
            if read_file:   # only add if not empty 
                rf.append(self.read_file_name(dir_path, extension))
        return rf
    # read, extract
    # TODO: optomise - find a better way
    def extract_yaml(self, data):
        """extract from list, yaml or F"""
        if not data:
            return False
        lines = data.split("\n")
        yaml_start = False
        yaml_end = False
        yaml = []
        count = 0
        for line in lines:
            if line == '---':
                yaml_start = True
                count += 1
            if yaml_start:
                if line != '---':
                    if line: 
                        data = line.split(":")
                        yaml.append({data[0]:data[1]})
                else:
                    if count > 1:
                        yaml_end = True
            if yaml_end:
                break
        if len(yaml) > 0:
            return yaml
        else:
            return False
    def extract_yaml_tags(self, tags):
        """
        extract from yaml['tags'], split by space, 
        return as list OR F
        """
        ytags = []
        if tags:
            tags = tags.split(" ")
            for tag in tags:
                ytags.append(tag)
            return ytags
        return False
    def extract_yaml_date(self, date):
        """extract date using Date8601"""
        if self.date8601.validate(date):
            (year, month, month_mm, month_mmm, day, hour, minute) = self.date8601.crack()
            return dict(year = year,
                        month = month,
                        month_mm = month_mm,  # mm 10
                        month_mmm = month_mmm, # mmm OCT
                        day = day,
                        hour = hour,
                        minute = minute)
        return False
    # tags
    def update_tags(self, item, tags):
        """update tag in tags list - remember, 
           tag list returns unchanged, even on 
           failure=
        """
        if item:
            if item not in tags:    # remove duplicates
                tags.append(item)
        return tags
    # read files
    def read(self, file_dir=""):
        """read source directory & slurp up filenames"""
        # no file directory supplied, assume preset
        # slurp files, build 'file directory + path + glob.ext'
        if self.is_dir_valid(file_dir):
            self.source_dir = file_dir        # valid, save for later
            self.filepath = []                # init filepath storage
            self.filepaths = self.read_file_names(self.source_dir)
            # only if there's a file
            if len(self.filepaths) > 0:
                # we have the filename, now the contents
                data = ""
                for fpn in self.filepaths:
                    data = self.read_file_content(fpn[0])
                    if data:
                        # yaml
                        tags = []
                        title = ""
                        description = ""
                        date = ""
                        is_markdown = False
                        is_displayed = False

                        # extract yaml
                        self.yaml = self.extract_yaml(data)
                        if self.yaml:
                            for yaml in self.yaml:
                                # tags
                                if 'tags' in yaml:
                                    tags = self.extract_yaml_tags(yaml['tags'])
                                # title
                                if 'title' in yaml:
                                    title = yaml['title'].replace("-"," ") # strip for display
                                # description
                                if 'description' in yaml:
                                    description = yaml['description']
                                # markdown
                                if 'markdown' in yaml:
                                    is_markdown = yaml['markdown']
                                # displayed
                                if 'displayed' in yaml:
                                    is_displayed = yaml['displayed']
                                if 'date' in yaml:
                                    date = yaml['date']
                                else:
                                    date = self.date8601.now()

                        # --- build list of file data --- 
                        # yaml date found?
                        # TODO add yyyy yyyymm yyyymmm yyyymmdd yyyymmmdd
                        #      add epoch to allow sorting by datetime
                        dt = self.extract_yaml_date(date)
                        #index_utc = dt['index_utc']
                        year = dt['year']
                        month_mm = dt['month_mm']
                        month = month_mm
                        month_mmm = dt['month_mmm']
                        day = dt['day']
                        hour = dt['hour']
                        minute = dt['hour']
                        
                        # tags
                        tags = self.update_tags(year, tags)
                        tags = self.update_tags(month_mm, tags)
                        tags = self.update_tags(month_mmm, tags)
                        tags = self.update_tags(day, tags)
                        tags = self.update_tags(hour, tags)
                        tags = self.update_tags(minute, tags)

                        # --- build dict of post data ---
                        p = dict(#index=index_utc,     # utc epoch of post date
                                 contents=data,       # body of post
                                 filepath=fpn,        # filepath of post
                                 datetime=dt,         # ???
                                 year=year,           # YYYY
                                 month=month,         # mm
                                 month_mmm=month_mmm, # mmm
                                 month_mm=month_mm,   # mm
                                 day=day,             # dd
                                 hour=hour,           # hh
                                 minute=minute,       # mm
                                 tags=tags,           # list of tags
                                 title=title,         # post title
                                 ext='html',           
                                 description=description, # 200 char summary
                                 markdown=is_markdown,    # bool, is markdown
                                 displayed=is_displayed)  # bool, do u show?
                        self.post.append(p)
                        # --- build list of post data ---
            self.post.sort()
            return True
        else:
            return False
    # processing
    def is_processed(self):
        """status of processing, set when completed processing, T/F"""
        return self.is_raw
    def create_directory(self, path):
        """create destination directory or F"""
        if not os.path.isdir(path):
            os.mkdir(path)
            return True
        else:
            return False        
    def process(self, destination_dir):
        """process source files into datastructure"""
        # we need a valid destination, don't make a directory
        if os.path.isdir(destination_dir):
            if self.post:
                self.post.sort()
                for post in self.post:
                    # destination
                    self.dest_dir = destination_dir

                    # file
                    filename = post['title']
                    ext = post['ext']

                    # dates
                    year = "%s" % post['year']
                    month = post['month_mmm']
                    day = "%s" % post['day']

                    # flags
                    is_markdown = post['markdown']
                    displayed = post['displayed']

                    if is_markdown:
                        data = "" # process markdown
                    else:
                        data = ""
 
                    # --- unroll process list building ---
                    # build each directory and index page in each index pointing
                    # to child files. 
                
                    # directories
                    dyyyy = os.path.join(self.dest_dir, year)
                    dyyyy_mmm = os.path.join(self.dest_dir, year, month)
                    dyyyy_mmm_dd = os.path.join(self.dest_dir, year, \
                                                month, day)
                
                    print(dyyyy)
                    print(dyyyy_mmm)
                    print(dyyyy_mmm_dd)

                    # create directories
                    print("destination <%s>" % self.dest_dir)
                    if not self.create_directory(dyyyy):
                        print("warning: fail to make YYYY destination directory")
                        print("\t%s" % dyyyy)
                        return False

                    if not self.create_directory(dyyyy_mmm):
                        print("warning: fail to make YYYYMMM destination directory")
                        print("\t%s" % dyyyy_mmm)
                        return False

                    if not self.create_directory(dyyyy_mmm_dd):
                        print("warning: fail to make YYYYMMMDD destination directory")
                        print("\t%s" % dyyyy_mmm_dd)
                        return False

                    # save content
                   # check file, ok, move along
            print("ok")
            return True    
        else:
            return False



# main entry point
def main():
    usage = "usage: %prog [v] -s -d"
    parser = OptionParser(usage)

    # --- options --- 
    parser.add_option("-s", "--source", dest="src_dir",
                      help="supply source directory to read files from")
    parser.add_option("-d", "--destination", dest="dest_dir", 
                      help="supply destination directory to save files too")
    parser.add_option("-v", "--version", dest="version",
                      action="store_true",
                      help="current version")    
    options, args = parser.parse_args()

    # --- process ---
    if options.src_dir:
        if os.path.isdir(options.src_dir):
            print("source <%s>" % options.src_dir)
            if options.dest_dir:
                if os.path.isdir(options.dest_dir):
                    # the business
                    dt = DateIso8601("")

                    ng = Nextgen(dt)
                    ng.source(options.src_dir)
                    ng.read()

                    for f in ng.file_path:
                        print("\t%s" % f)
                    print("destination <%s>" % options.dest_dir)
                    if ng.yaml:
                        print("\t%s yaml" % len(ng.yaml))
                    else:
                        print("\tno yaml")

                    print("\t%s post" % len(ng.post))
                    #for p in ng.post:
                    #    print("\t", p)
                    #    print("\n")

                    print("process")
                    if ng.process(options.dest_dir):
                        print("ok")
                    else:
                        print("error: problems processing")
                        print("\t<%s>" % options.dest_dir)
                        sys.exit(1)
                    dt = None
                    ng = None
                else:
                    print("error: must supply a valid <destination directory>")
                    print("\t<%s>" % options.dest_dir)
                    sys.exit(1)
            else:
                    parser.print_help()
                    print("\nerror: must supply a <destination directory>")
                    sys.exit(1)                
        else:
            print("error: must supply a valid <source directory>")
            print("\t<%s>" % options.src_dir)
            sys.exit(1)
    else:
        parser.print_help()
        print("\nerror: must supply a <source directory>")
        sys.exit(1)


#---
# main app entry point
#--- 
if __name__ == '__main__':
    main()


# vim: ff=unix:ts=4:sw=4:tw=78:noai:expandtab
