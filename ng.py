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
import shutil
import os.path
import datetime
from optparse import OptionParser


import markdown2


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
        """initialise variables and set up structures"""
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
            return self.year, self.month, \
                   self.month_mm, self.month_mmm, self.day, \
                   self.hour, self.minute
        else: 
            return False
    def epoch(self):
        """return ISO6601 as epoch"""
        if self.is_valid:
            t = datetime.datetime(self.year, self.month, 
                                  self.day, self.hour, 
                                  self.minute)
            self.epoch = "%s" % time.mktime(t.timetuple())
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
        self.index = []
        self.yaml = []
    # extract
    def extract_content(self, yaml_count, data):
        """
        given end of yaml, line number, count until end, 
        then extract all data afterwards as list
        """
        if not data:
            return False
        counter = 0
        lines = data.split("\n")
        post = ""
        for line in lines:
           if counter > yaml_count + 1:
                post = "%s\n%s" % (post, line)
           counter += 1
        return post
    # TODO: optomise - find a better way
    def extract_yaml(self, data):
        """
        extract from data, yaml or F by searching for
        start and end of yaml, '---' and return as list
        """
        if not data:
            return False
        lines = data.split("\n")
        yaml_start = False
        yaml_end = False
        yaml = []
        count = 0
        for line in lines:  # TODO much craziness, fix this quickly
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
            (year, month, month_mm, month_mmm, 
             day, hour, minute) = self.date8601.crack()
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
            if item not in tags:    # no dupes
                tags.append(item)
        return tags
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
    def directory(self, path, is_create):
        """create or delete directory path"""
        if is_create:
            if not os.path.isdir(path):
                os.mkdir(path)
                return True
            else:
                return False
        else:
            if os.path.isdir(path):
                # DANGER Will Robinson, DANGER
                shutil.rmtree(path)
                return True
            else:
                return False
    def create_directory(self, path):
        """create destination directory or F"""
        return self.directory(path, True)
    def remove_directory(self, path):
        """remove directory & everything below it"""
        return self.directory(path, False)
    # file paths
    def path_build(self, lst_paths):
        """build a path from list of path fragments"""
        path = ""
        for p in lst_paths:
            path = os.path.join(path, str(p))
        return path
    # read 
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
        fn = []
        for filename in fpn:
            if filename:
                fn.append(filename)
        return fn
    def read_file_names(self, dir_path):
        """read filepath names by file extension, flatten lists to list"""
        rf = []
        for extension in self.ext:
            fn = self.read_file_name(dir_path, extension)
            if len(fn) > 0:
                for filename in fn:
                    if filename: 
                        rf.append(filename)
        return rf
    def read(self, file_dir=""):
        """read source directory & slurp up filenames"""
        # slurp files, build 'file directory + path + glob.ext'
        if self.is_dir_valid(file_dir):
            self.source_dir = file_dir        # valid, save for later
            self.filepath = []                # init filepath storage
            self.filepaths = self.read_file_names(self.source_dir)
            # only if there's a file
            if len(self.filepaths) > 0: # this is a list
                data = ""
                index_data = [] # build list of index data
                # epoch, title, abstract, year, mmm, day, hh, mm, dt, path
                
                # we have the filename, now the contents
                for fpn in self.filepaths:
                    data = self.read_file_content(fpn)
                    if data:
                        # yaml
                        tags = []
                        title = ""
                        description = ""
                        abstract = "" # TODO where is this being extracted?
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
                                    # strip for display
                                    title = yaml['title'].replace("-"," ") 
                                # description
                                if 'description' in yaml:
                                    description = yaml['description']
                                # markdown
                                if 'markdown' in yaml:
                                    is_markdown = yaml['markdown']
                                # displayed
                                if 'displayed' in yaml:
                                    is_displayed = yaml['displayed']
                                # TODO hey bonehead!
                                #      are you extracting date from the 
                                #      filename? if not, do so
                                if 'date' in yaml:
                                    date = yaml['date']
                                else:
                                    # --- OVER HERE ---
                                    date = self.date8601.now()

                        # --- build list of file data --- 
                        # yaml date found?
                        # TODO add yyyy yyyymm yyyymmm yyyymmdd yyyymmmdd
                        #      add epoch to allow sorting by datetime
                        dt = self.extract_yaml_date(date)
                        if dt:
                            # datetime
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


                            # post content
                            yml_count = len(self.yaml)
                            c = self.extract_content(yml_count, data)
                            # --- build dict of post data ---
                            p = dict(#index=index_utc,    # utc epoch of post date
                                 content=c,           # body of post
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
                                 postpath="",         # post path
                                 title=title,         # post title
                                 description=description, # 200 char summary
                                 content_processed="",# content thru markdown
                                 ext='html',          # content filename ext
                                 markdown=is_markdown,    # bool, is markdown
                                 displayed=is_displayed)  # bool, do u show?

                            self.post.append(p)                            
                            # --- end build ---
                            # --- build dict of link data ---
                            link = dict(title=title,
                                        abstract=abstract,
                                        file_path="",
                                        year="",
                                        mmm=month_mmm,
                                        day=day,
                                        dt_format="",
                                        dt_epoch="",
                                        hour=hour,
                                        minute=minute)

                            self.index.append(link)
                            # --- end build
            # TODO problem here
            return True
        else:
            return False
    # processing
    def process(self, destination_dir):
        """process source files into datastructure"""
        # we need a valid destination, don't make a directory
        if os.path.isdir(destination_dir):
            if self.post:
                for post in self.post:
                    # destination
                    self.dest_dir = destination_dir
                    # --- process markdown ---
                    if post['markdown']:
                        if post['content']:
                            md = markdown2.markdown(post['content'])
                            post['content_processed'] = md # process markdown
                        else:
                            post['content_processed'] = ""
                    else:
                        pass

                    # --- dates ---
                    year = "%s" % post['year']
                    mmm = post['month_mmm']
                    mm = post['month_mm']
                    day = "%s" % post['day']

                    # --- directories ---
                    path_yyyy = self.path_build([year])
                    post['path_yyyy'] = path_yyyy
                    
                    path_yyyymm = self.path_build([year, mm])
                    post['path_yyyymm'] = path_yyyymm

                    path_yyyymmdd = self.path_build([year, mm, day])
                    post['path_yyyymmdd'] = path_yyyymmdd

                    path_yyyymmm = self.path_build([year, mmm])
                    post['path_yyyymmm'] = path_yyyymmm

                    path_yyyymmmdd = self.path_build([year, mmm, day])
                    post['path_yyyymmmdd'] = path_yyyymmmdd
                    post["postpath"] = path_yyyymmmdd
                    #
                    # --- end directories ---
            return True    
        else:
            return False
    def save(self):
        """ """
        # for post in posts
        #     build directory
        #         build file
        #file = dict(filename=filename,
        #            ext=extension,
        #            title=title,
        #            abstract=description,
        #            tags=[],
        #            date=date,
        #            path=path,
        #            body=content)
                    
                    
        #             filename + ext
        #             summary from description
        #             title
        #             tags
        #             path via year, month, day
        #             time hour, minute
        #             body
        #             
        #         build index
        #             title
        #             path
        #             summary
        #             date time
        #         save file
        #    save index files
        #     
        pass



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
                    if ng.read(options.src_dir):
                        for f in ng.filepath:
                            print("\t%s" % f)
                        print("destination <%s>" % options.dest_dir)
                        if not ng.process(options.dest_dir):
                            print("error: problems processing")
                            print("%s <%s>" % options.dest_dir)
                            sys.exit(1)
                        print("process")
                        count = 1
                        for p in ng.post:
                            print("%s %s: %s" % (count, p['title'], p['description']))
                            count += 1
                        print("save")
                        ng.save()
                        dt = None
                        ng = None
                    else:
                        print("error: problems reading data")
                        print("\t<%s>" % options.src_dir)
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
