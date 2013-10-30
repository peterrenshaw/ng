#!/usr/bin/env python
# ~*~ encoding: utf-8 ~*~


#===
# name: site.py
# date: 2013OCT09
# prog: pr
# desc: quick hack for a not so nextgen 
#       static html site generator
#===


import os
import glob
import time
import os.path
from string import Template


import markdown2


import ng.page
import ng.tools

from ng.page import Page
from ng.page import Container
from ng.tools import DateIso8601


# --- Nextgen object ---
#

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
    def __init__(self, d8601=DateIso8601(),
                       container=Container()):
        """inject Date object, init variables"""
        # objects
        self.date8601 = d8601    # 
        self.link = container   # container for Index of dict to sort

        # paths
        self.source_dir = ""
        self.dest_dir = ""
        self.ext = ["md","markdown","txt"]
        self.filepath = []

        # --- data source ---
        # static 
        self.site = {}  # site information, no change
        self.yaml = []  # yaml data from source post file
  
        # dynamic
        self.post = []  # data from post
        self.page = []  # Page object with post data
        self.index = [] # link data from index object
        # --- end data source ---
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
                        # --- Important ---
                        # split takes into account yaml *date* format
                        # in effect, splits line left (key) and right
                        # (value) by ':'
                        # --- Important ---
                        data = line.split(":", maxsplit=1)  
                        yaml.append({data[0].strip():data[1].strip()})
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
            (epoch, year, month, month_mm, month_mmm, 
             day, hour, minute) = self.date8601.crack()
            return dict(epoch = epoch,
                        year = year,
                        month = month,         # mm 10
                        month_mm = month_mm,   # mm 10
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
    def file_name(self, filename, ext=""):
        """process and build filename"""
        if filename:
           fn = ng.tools.remove_char(value=filename)
           fn = fn.strip()

           # we don't want to remove the dash, "-"
           # as it makes the title easier to read
           fn = fn.replace(" ","-")
           fn = fn.lower()

           # build filename
           if ext:
               fn = "%s.%s" % (fn, ext)
           
           return fn
        return False
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
                
                # TODO should be as config file & populated via 
                #      method, otherwise just store
                self.site = dict(author = "Peter Renshaw", 
                                 name = "Seldomlogical",
                                 byline = "new ideas, ideal \
                                          solutions are seldom\
                                          logical. attaining \
                                          a desired goal \
                                          always is")
                
                # we have the filename, now the contents
                for fpn in self.filepaths:
                    data = self.read_file_content(fpn)
                    if data:
                        # yaml
                        tags = []
                        title = ""
                        filename = ""
                        ext = "html"
                        description = ""
                        abstract = ""
                        date = ""
                        is_markdown = False
                        is_displayed = False
                        self.yaml = []

                        # extract yaml
                        self.yaml = self.extract_yaml(data)
                        if self.yaml:
                            for yaml in self.yaml:
                                # tags
                                if 'tags' in yaml:
                                    tags = self.extract_yaml_tags(yaml['tags'])
                                # title
                                # filename
                                if 'title' in yaml:
                                    # strip for display
                                    title = yaml['title']
                                    title = title.strip()
                                # abstract
                                if 'abstract' in yaml:
                                    abstract = yaml['abstract']
                                    abstract = abstract.strip()
                                # description
                                if 'description' in yaml:
                                    description = yaml['description'].strip()
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
                                #else:
                                    # --- OVER HERE ---
                                    #date = self.date8601.now()
                                    #print("2 date=<%s>" % date)


                        # --- build list of file data --- 
                        # yaml date found?
                        # TODO add yyyy yyyymm yyyymmm yyyymmdd yyyymmmdd
                        #      add epoch to allow sorting by datetime
                        
                        # IF NO DT FOUND THIS WILL CRASH
                        # if there's no yaml datetime, 
                        # datetime information can come from?
                        #     - filename
                        #     - file system timestamp
                        #     - current datetime
                        # scenario:
                        #     * blog entry
                        #     - use datetime for paths
                        #     * static page  
                        #     - off root page
                        dt = self.extract_yaml_date(date)
                        if not dt:
                            print("Error: datetime problem in nextgen.read")
                            return False
                        else:
                            # datetime
                            epoch = float(dt['epoch'])
                            year = int(dt['year'])
                            month_mm = int(dt['month_mm'])
                            # set month as 'nn',n is integer
                            month = int(dt['month_mm']) 
                            month_mmm = dt['month_mmm']
                            day = int(dt['day'])
                            hour = int(dt['hour'])
                            minute = int(dt['minute'])
                            epoch = float(dt['epoch'])
                        
                            # tags
                            tags = self.update_tags(year, tags)
                            tags = self.update_tags(month_mm, tags)
                            tags = self.update_tags(month_mmm, tags)
                            tags = self.update_tags(day, tags)
                            tags = self.update_tags(hour, tags)
                            tags = self.update_tags(minute, tags)

                            # TODO build_filepath
                            # move filepath for page, to Page object
                            filename = self.file_name(title)
                            filepath = os.path.join(str(year), month_mmm, str(day))
                            relpath = "%s/%s/%s" % (str(year), month_mmm, str(day))

                            # post content
                            yaml_count = len(self.yaml) if self.yaml else 0
                            c = self.extract_content(yaml_count, data)
                            # --- build dict of post data ---
                            p = dict(#index=index_utc,     # utc epoch of post date
                                 content=c,                # body of post
                                 basepath="",              # destination path
                                 filepath=filepath,        # filepath of post
                                 relpath=relpath,
                                 filename=filename,        # filename
                                 datetime=dt,              # empty at moment, 
                                                           # strf formatted datetime
                                 year=year,                # YYYY
                                 month=month,              # assume mm, if not set
                                 month_mmm=month_mmm,      # mmm
                                 month_mm=month_mm,        # mm
                                 day=day,                  # dd
                                 hour=hour,                # hh
                                 minute=minute,            # mm
                                 tags=tags,                # list of tags
                                 title=title,              # post title
                                 abstract=abstract,        # 140 char summary
                                 content_processed="",     # empty at moment, 
                                                           # content thru markdown
                                 ext=ext,                  # content filename ext
                                 markdown=is_markdown,     # bool, is markdown
                                 displayed=is_displayed)   # bool, do u show?

                            self.post.append(p)                            
                            # --- end build ---

                            # TODO epoch and strf are from???
                            # --- build dict of link index data ---
                            self.link.add(title=title,
                                          abstract=abstract,
                                          filename=filename,
                                          filepath=filepath,
                                          relpath=relpath,
                                          year=year,
                                          month_mmm=month_mmm,
                                          day=day,
                                          dt_epoch=epoch,
                                          hour=hour,
                                          minute=minute)
                            # --- end build

            # TODO problem here
            return True
        else:
            return False
    def read_partial(self, name, source=""):
        """read partial pages (templates) from source"""
        if source:
            cur_dir = source
        else:
            cur_dir = self.source_dir
        if os.path.isdir(cur_dir):
            if name:
                tpl = False
                fpn = os.path.join(cur_dir, 'partials', name)
                if os.path.isfile(fpn):
                    with open(fpn, encoding='utf-8') as f:
                       tpl = f.read()
                    f.close()
                return tpl
        return False
    # processing
    def process(self, destination_dir):
        """process source files into datastructure"""
        # we need a valid destination, don't make a directory
        if os.path.isdir(destination_dir):
            if self.post:
                # load header, footer
                tpl_header = self.read_partial('header.html')
                tpl_footer = self.read_partial('footer.html')
                tpl_content = self.read_partial('content.html')
        
                if not (tpl_header and tpl_footer and tpl_content):
                    print("templates are %s" % (tpl_header and 
                                                tpl_footer and 
                                                tpl_content))
                    print("header is %s" % tpl_header)
                    print("footer is %s" % tpl_footer)
                    print("content is %s" % tpl_content)
                    return False

                for post in self.post:
                    # destination
                    self.dest_dir = destination_dir

                    # --- process markdown ---
                    if post['markdown']:
                        if post['content']:
                            md = markdown2.markdown(post['content'])
                            post['content_processed'] = md # process markdown
                        else:
                            post['content_processed'] = post['content']
                    else:
                        post['content_processed'] = post['content']


                    # --- dates ---
                    year = int(post['year'])
                    month_mmm = post['month_mmm']
                    month_mm = int(post['month_mm'])
                    month = post['month']
                    day = int(post['day'])
                    hour = int(post['hour'])
                    minute = int(post['minute'])

                    if ng.tools.dt_is_valid_input(year, month_mm, 
                                                  day, hour, minute):
                        pass
                    else:
                        print("error: time problems in site.Nextgen")
                        status = ng.tools.dt_is_valid_input(year, month_mm, 
                                                            day, hour, minute)
                        print("STATUS is %s" % status)
                        print(year, month_mm, day, hour, minute)
                        print("year is %s" % year)
                        print("month_mm is %s" % month_mm)
                        print("month_mmm is %s" % month_mmm)
                        print("month is %s" % month)
                        print("day is %s" % day)
                        print("hour is %s" % hour)
                        print("minute is %s" % minute)
                        return False

                    # --- body ---
                    title = post['title']
                    abstract = post['abstract']
                    content = post['content_processed']          

                    # --- paths ---
                    filename = post['filename']
                    filepath = post['filepath']
                    relpath =  post['relpath']
                    
                    # --- directories ---
                    path_yyyy = self.path_build([year])
                    post['path_yyyy'] = path_yyyy
                    
                    path_yyyymm = self.path_build([year, month_mm])
                    post['path_yyyymm'] = path_yyyymm

                    path_yyyymmdd = self.path_build([year, month_mm, day])
                    post['path_yyyymmdd'] = path_yyyymmdd

                    path_yyyymmm = self.path_build([year, month_mmm])
                    post['path_yyyymmm'] = path_yyyymmm

                    path_yyyymmmdd = self.path_build([year, month_mmm, day])
                    post['path_yyyymmmdd'] = path_yyyymmmdd
                    post["postpath"] = path_yyyymmmdd
                    #
                    # --- end directories ---

                    # --- build pages ---
                    # page object
                    page = ng.page.Page(is_index=True)

                    # templates
                    page.header(tpl_header)
                    page.footer(tpl_footer)
                    
                    # content of index

                    # data
                    # year, month, day, hour, minute, [strf_format]
                    dt_epoch = ng.tools.dt_ymdhm2_epoch(year=year,
                                                        month_mm=month_mm,
                                                        day=day,
                                                        hour=hour,
                                                        minute=minute)
                    dt_strf = ng.tools.dt_ymdhm2_strf(year=year,
                                                      month=month_mm,
                                                      day=day,
                                                      hour=hour,
                                                      minute=minute)
                    page.timedata(dt_epoch=dt_epoch,
                                   year=year,
                                   month_mm=month_mm,
                                   month_mmm=month_mmm,
                                   month=month,
                                   day=day,
                                   hour=hour,
                                   minute=minute,
                                   dt_strf=dt_strf)
                    page.filedata(basepath=self.dest_dir,
                                   relpath=relpath,
                                   name=filename, 
                                   ext="html")
                    tags=[self.site['author'].replace(" ","").lower(), 
                          self.site['name'].replace(" ","").lower(),
                          post['year'], post['month_mm'], post['day'], 
                          post['hour'], post['minute']]
                    page.metadata(tags=tags,
                                   author=self.site['author'],
                                   site_name=self.site['name'],
                                   site_byline=self.site['byline'],
                                   is_index=True)
                    page.body(title=title,
                               abstract=abstract,
                               content=content,
                               template=tpl_content)
                    if False:
                        print("=== TESTING ===")
                        status = not ng.tools.dt_is_valid_input(year, month_mm, day, hour, minute)
                        print("STATUS is %s" % status)
                        print(year, month_mm, day, hour, minute)
                        print("year is %s" % year)
                        print("month_mm is %s" % month_mm)
                        print("month_mmm is %s" % month_mmm)
                        print("day is %s" % day)
                        print("hour is %s" % hour)
                        print("minute is %s" % minute)

            return True    
        else:
            print("post=<%s>" % self.post)
            return False
    def save(self):
        """save posts and index to file"""
        # save index first
        """if self.link.sort(term='dt_epoch'):
            for link in self.link.all():
                for key in link.keys():
                    print("link %s='%s'" % (key, link[key]))
        else:
            print("Error: link problems")
            print("\tlink=%s" % self.link)
        """
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
#
# --- end Nextgen object ---


#---
# main:  
#---
def main():
    pass


#---
# main app entry point
#--- 
if __name__ == '__main__':
    main()


# vim: ff=unix:ts=4:sw=4:tw=78:noai:expandtab
