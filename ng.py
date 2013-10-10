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
# dt_iso_valid: check  if "YYYY-MM-DDTHH:MM:SS T/F"
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
    """break ISO8601 into time components"""
    year = int(dts[0:4])
    month = int(dts[5:7])
    day = int(dts[8:10])
    hh = int(dts[14:16])
    mm = int(dts[17:19])
    return year, month, day, hh, mm
# dt_str_8601_to_epoch: generates 1381352400.0 from YYYY-MM-DDTHH:MM:SS
def dt_str_8601_to_epoch(year, month, day, hour, minute):
    """convert YYYY-MM-DDTHH:MM:SS to epoch"""
    t = datetime.datetime(year, month, day, hour, minute)
    return time.mktime(t.timetuple())
# dt_str_8601_to_date: generates for eg: 2013-10-10
def dt_str_8601_to_date(year, month, day):
    """return generates YYYY-MM-DD"""
    return datetime.date(year, month, day)
# dt_iso_8601_utc: generates utc: 1381339265.0
def dt_iso_8601_utc():
    """return generates utc: 1381339265.0"""
    t = datetime.datetime.utcnow()
    return time.mktime(t.timetuple())
# dt_iso_8601_utc_offset: generates utc+offset 138137865.0
def dt_iso_8601_utc_offset():
    t = datetime.datetime.now()
    return time.mktime(t.timetuple())
#
# --- end time tools ---


#===
# name: Nextgen
# date: 2013OCT09
# prog: pr
# desc: hack an old, nextgeneration static blog
#       engine in 8 hrs
# usge: 
#            ng = Nextgen()
#            ng.source(<source directory>)
#            ng.destination(<destination directory>)
#            ng.process()
#===
class Nextgen:
    def __init__(self):
        self.source_dir = ""
        self.dest_dir = ""
        self.ext = ["md","markdown","txt"]
        self.filepath = []
        self.post = []
        self.is_raw = True
        self.yaml = []
    # directories
    def directory(self, file_dir=""):
        """valid directory or F"""
        if file_dir:
            if os.path.isdir(file_dir):
                return file_dir
        return False
    def source(self, file_dir=""):
        """valid source directory or F"""
        sdp = self.directory(file_dir)
        if sdp: 
            self.source_dir = sdp
            return True
        else:
            return False
    def destination(self, file_dir=""):
        """valid destination directory or F"""
        fdp = self.directory(file_dir)
        if fdp: 
            self.dest_dir = fdp
            return True
        else:
            return False
    # filepaths
    def file_paths(self):
        """return list of filepaths or F"""
        if len(self.filepath) > 0: return self.filepath
        else: return False
    def read_file(self, filename):
        """read file contents or F"""
        if os.path.isfile(filename):
           data = ""
           f = None
           try: 
               with open(filename, encoding='utf-8') as f:
                   data = f.read()
               f.close()
               return data
           except:
               data = ""
               if f: f.close()
        return False
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
        """extract from yaml['tags'], split by space and return as list OR F"""
        ytags = []
        if tags:
            tags = tags.split(" ")
            for tag in tags:
                ytags.append(tag)
            return ytags
        return False
    def extract_yaml_date(self, date):
        """extact date into dict or F"""
        if date:
            month = {'JAN':'01','FEB':'02','MAR':'03','APR':'04',
                     'MAY':'05','JUN':'06','JUL':'07','AUG':'08',
                     'SEP':'09','OCT':'10','NOV':'11','DEC':'12'}
            if len(date) == len("YYYYMMMDDTHHMM"):
                if date[9] == 'T':
                    yyyy = date[0:4]
                    mmm = date[4:7]
                    mon = month[mmm]  # OCT to 10
                    dd = date[7:9]
                    hh = date[10:12]
                    mm = date[12:14]
                    return dict(year = yyyy,
                                month_mm = mon,  # mm 10
                                month_mmm = mmm, # mmm OCT
                                day = dd,
                                hour = hh,
                                minute = mm)
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
        # load source file directory 
        if file_dir:
            if not self.source(file_dir):
                return False

        # no file directory supplied, assume preset
        # slurp files, build 'file directory + path + glob.ext'
        if self.source_dir:
            self.filepath = []                # init filepath storage 
            for extension in self.ext:        # extract for each ext
                glob_ext = "*.%s" % extension # build extension, filepath glob, *.foo
                gfp = os.path.join(self.source_dir, glob_ext)

                # returns list of filepaths
                # <http://www.diveinto.org/python3/comprehensions.html#os>
                fpn = [os.path.realpath(f) for f in glob.glob(gfp)]
                if fpn: 
                    self.filepath = fpn

            # only if there's a file
            if self.filepath:
                # we have the filename, now the contents
                data = ""
                for fpn in self.filepath:
                    data = self.read_file(fpn)
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

                        # --- build list of file data --- 
                        # yaml date found?
                        # TODO add yyyy yyyymm yyyymmm yyyymmdd yyyymmmdd
                        #      add epoch to allow sorting by datetime
                        if date:
                            dt = self.extract_yaml_date(date)
                            year = dt['year']
                            tags = self.update_tags(year, tags)
                            month_mm = dt['month_mm']
                            tags = self.update_tags(month_mm, tags)
                            month_mmm = dt['month_mmm']
                            tags = self.update_tags(month_mmm, tags)
                            day = dt['day']
                            tags = self.update_tags(day, tags)
                            hour = dt['hour']
                            tags = self.update_tags(hour, tags)
                            minute = dt['hour']
                            tags = self.update_tags(minute, tags)
                        else:
                            # TODO fix no date tags 
                            t = datetime.datetime.utcnow()
                            dt = time.mktime(t.timetuple())
                            year = ""
                            month_mm = ""
                            month_mmm = ""
                            day = ""
                            hour = ""
                            minute = ""
                        tags.sort()

                        # --- build dict of post data ---
                        p = dict(contents=data,
                                 filepath=fpn,
                                 datetime=dt,
                                 year=year,
                                 month_mmm=month_mmm,
                                 month_mm=month_mm,
                                 day=day,
                                 hour=hour,
                                 minute=minute,
                                 tags=tags,
                                 title=title,
                                 ext='html',
                                 description=description,
                                 markdown=is_markdown,
                                 displayed=is_displayed)
                        self.post.append(p)
                        # --- build list of post data --- 
                if self.post: return True
        return False
    # processing
    def is_processed(self):
        """status of processing, set when completed processing, T/F"""
        return self.is_raw
    def create_directory(self, path):
        """create destination directory or F"""
        if not os.path.isdir(path):
            os.mkdir(path)
        else:
            return False        
    def process(self, destination_dir):
        """process source files into datastructure"""
        # we need a valid destination, don't make a directory
        if os.path.isdir(destination_dir):
            self.dest_dir = destination_dir
        else:
            return False

        if self.post:
            for post in self.post:
                # file
                filename = post['title']
                ext = post['ext']

                # directory
                dir_year = post['year']
                dir_month = post['month_mmm']    # mm or mmm? give option?
                dir_day = post['day']

                # flags
                is_markdown = post['markdown']
                displayed = post['displayed']

                if is_markdown:
                    data = "" # process markdown
                else:
                    data = ""
                
                # dates
 
                # --- unroll process list building ---
                # build each directory and index page in each index pointing
                # to child files. 
                
                # directories
                dyyyy = os.path.join(self.dest_dir, dir_year)
                dyyyy_mmm = os.path.join(self.dest_dir, dir_year, dir_month)
                dyyyy_mmm_dd = os.path.join(self.dest_dir, dir_year, dir_month, dir_day)
                
                # create directories
                print("destination <%s>" % self.dest_dir)
                if self.create_directory(dyyyy):
                    print("\ts" % dyyyy)
                else:
                    print("\t%s" % dyyyy)
                if self.create_directory(dyyyy_mmm):
                    print("\t%s" % dyyyy_mmm)
                else:
                    print("\t%s" % dyyyy_mmm)
                if self.create_directory(dyyyy_mmm_dd):
                    print("\t%s" % dyyyy_mmm_dd)
                else:
                    print("\t%s" % dyyyy_mmm_dd)

                # save content
                
                # check file, ok, move along
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
                    ng = Nextgen()
                    ng.source(options.src_dir)
                    ng.read()
                    p = ng.file_paths()
                    print("%s paths" % len(p))
                    for f in p:
                        print("\t%s" % f)
                    print("destination <%s>" % options.dest_dir)
                    print("yaml")
                    if ng.yaml:
                        print("%s yaml" % len(ng.yaml))
                        print(ng.yaml)
                    else:
                        print("no yaml")

                    print("%s post" % len(ng.post))
                    for p in ng.post:
                        print(p)
                        print("\n")
      
                    print("process")
                    if ng.process(options.dest_dir):
                        print("ok")
                        
                    else:
                        print("error: problems processing")
                        print("\t<%s>" % options.dest_dir)
                        sys.exit(1)

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
