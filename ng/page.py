#!/usr/bin/env python
# ~*~ encoding: utf-8 ~*~


#===
# name: page.py
# date: 2013OCT09
# prog: pr
# desc: quick hack for a not so nextgen 
#       static html site generator
#===


import os
import time
from string import Template


import ng.tools # build_respath


# ---- Container object ---
#

#===
# name: Container
# date: 2013OCT24
# prog: pr
# desc: using only list and dictionary, sort the list of
#       dictionary values by key. The object allows you to 
#       add multiple dictionaries of data (test) then sort by 
#       existing key. Add a dictionary, every dictionary after
#       this must have the same keys, this is enforced on add.
#
#       funky :)
#===
class Container:
    def __init__(self):
        """initialise variables"""
        self.index = []
    def add(self, **kwargs):
        """
        enter multiple key=value items, convert to dict
        save to master index - clear dict for next add
        First add will dicate all other keys allowed
        """
        data = {}
        if kwargs:
            for key in kwargs:
                # is key valid ie: is key found 
                # in first add? are sucessive add's
                # have same keys as first?
                if self.valid(key):
                    data[key] = kwargs[key]
                else:
                    return False
            self.index.append(data)
            return True
        return False
    def valid(self, key):
        """
        is every keys entered exactly same as 
        keys in first add? if so T, else F
        """
        if len(self.index) >= 1:
            if key in self.index[0].keys():
                return True
            else:
                return False
        else:
            return True
    def sort(self, term, order=True):
        """return copy of list of sorted items by key or F"""
        # is *search term* in first item, of index?
        if term in self.index[0]:
            # force *order* to T/F
            if order is True or order is False: 
                # sort all dicts in list, by term and order
                items = sorted(self.all(), 
                               key = lambda data: data[term], 
                               reverse = order)
                return items
        return False
    def clear(self):
        """clears index list"""
        self.index = []
    def all(self, is_sort=False, key='dt_epoch'):
        """all index data in list"""
        if is_sort:
            if key in self.index:
                return self.sort(key)
        return self.index
#
# --- end container object --- 


# --- Page object ---
#

#===
# name: Page
# date: 2013OCT21
# prog: pr
# desc: model a Page to be saved
#===
class Page:
    def __init__(self, is_index):
        """initialise the Page"""
        self.is_index = (True if is_index else False)
        self.index = []             # list of index data for rendering
        self.prod_name = "nextgen"  # pass in
        self.prod_version = "0.1"   # pass in

        # basic page
        self.__header = ""     # template
        self.__footer = ""     # template
        self.__body = ""       # container for body

        # --- data types ---
        # list of dictionaries used to store below - use for checking 
        self.dtypes = ['body','file','header','image','index','meta','time']

        # body
        self.body_data = dict(title="",       # page title
                              abstract="",    # summary, <140 char
                              body="",        # entire text
                              template="")    # template for body
        # file
        self.file_data = dict(basepath="",    # root path 
                              relpath="",     # path relative to base
                              fullpath="",    # full path to file
                              respath="",     # reverse path to resources
                              name="",        # filename
                              ext="")         # filename extension
        # directory
        self.dir_data = []                    # directories

        # time
        self.time_data = dict(dt_epoch="",    # epoch
                              year="",        # year YYYY
                              month="",       # mmm or mm
                              month_mmm="",   # mmm == JAN, FEB, etc
                              month_mm="",    # mm == 01, 02, etc, zero pad
                              day="",         # 01, 02, etc zero pad
                              hour="",        # hour in HH format, zero pad
                              minute="",      # minute in MM fomat, zero pad
                              dt_strf="")     # string formatted date time
        # meta
        self.meta_data = dict(author="",              # author name
                              site_name="",           # name of site
                              site_byline="",         # site tag line
                              site_domain="",         # site domain name
                              prod_name="",           # name of product
                              prod_version="",        # product version no
                              tags=[],                # tags per Page
                              is_index=self.is_index) # is this an index?
        # image
        self.image_data = dict(img_url="",        # url to image for linking
                               img_src="",        # source url to image display
                               img_height="",     # image attribute
                               img_width="")      # image attribute
        #
        # --- end data types ---

        # --- mapping --- 
        # header
        self.header_map = dict(author="",
                               site_name="",
                               site_byline="",
                               site_domain="",
                               title="",
                               abstract="", 
                               year="",
                               month_mmm="",
                               month_mm="",
                               day="",
                               respath="",       # resources path
                               tool="",
                               version="")
        # body
        self.body_map = dict(title="",
                             site_name="",
                             site_byline="",         # site tag line
                             author="",
                             abstract="",
                             description="",
                             body="",
                             year="",
                             respath="",        # resources path
                             month_mmm="",
                             month_mm="",
                             day="", 
                             img_url="",
                             img_src="",
                             img_height="",
                             img_width="",
                             dt_strf="")
        # footer
        self.footer_map = dict(respath="")

        # index
        self.index_map = dict(title="",
                              abstract="",
                              file_path="",
                              year="",
                              month_mmm="",
                              day="",
                              hour="",
                              minute="",
                              dt_strf="",
                              dt_epoch="")
        # --- end mapping ---

    # --- collect data ---
    def header(self, content):
        """content for Page header"""
        if content:
            self.__header = content
            return True
        return False
    def body(self, title, abstract, content, template):
        """content for Page body"""
        if title:
            if abstract:
                if content:
                    if template:
                        title = self.q_body('title', data=title, is_set=True)
                        abstract = self.q_body('abstract', data=abstract, is_set=True)
                        body = self.q_body('body', data=content, is_set=True)
                        template = self.q_body('template', data=template, is_set=True)
                        return (title and abstract and body and template)
        return False
    def footer(self, content):
        """footer content, set or F"""
        if content:
            self.__footer = content
            return True
        return False
    def dirdata(self, directory):
        """build directory data"""
        if not directory in self.dir_data:
            self.dir_data.append(directory)
            return True
        else:
            return False
    def filedata(self, basepath, name, ext, relpath=""):
        """
        build page filename from paths, name & ext. remember
        that 'relpath' is optional so deal with this.
        """
        if os.path.isdir(basepath):
            if ext in ['html','htm','txt']:
                if name:
                    base = self.q_file('basepath', data=basepath, is_set=True)
                    name = self.q_file('name', data=name, is_set=True)
                    ext = self.q_file('ext', data=ext, is_set=True)
                    
                    if relpath:  # optional
                        rel = self.q_file('relpath', data=relpath, is_set=True)
                        status = (base and rel and name and ext)
                    else:
                        status = (base and name and ext)

                    # basepath, filename and extension valid?
                    if status: 
                        self.filepath()
                        return True
                    else:
                        return False
        return False
    def filepath(self):
        """
        build full filepath with filename and extension
        remember! this is building web server filepath but
        it could also be used on win32 so use 'os.path.join'
        also remember 'optional' relpath assume 'name' 
        and 'ext' valid.
        """
        if self.q_file('basepath'):
            if self.q_file('name') and self.q_file('ext'):
                fn = "%s.%s" % (self.q_file('name'), self.q_file('ext'))
                fullpath = ""
                relpath = self.q_file('relpath')
                if relpath:
                    fullpath = os.path.join(self.q_file('basepath'), relpath, fn)
                else:
                    fullpath = os.path.join(self.q_file('basepath'), fn)
                respath = ng.tools.build_respath(self.q_file('relpath')) 

                res =  self.q_file('respath', data=respath, is_set=True)
                full = self.q_file('fullpath', data=fullpath, is_set=True)

                return (res and full)

        return False
    def imagedata(self, source, url, height=375, width=500):
        """collect image data for main image, default HxW"""
        if source:
             if url:
                 source = self.q_image(key='img_src', data=source, is_set=True)
                 url = self.q_image(key='img_url', data=url, is_set=True)
                 height = self.q_image(key='img_height', data=height, is_set=True)
                 width = self.q_image(key='img_width', data=width, is_set=True)
                 return (source and url and height and width)
        return False
    def metadata(self, **kwargs):
        """
        lots of metadata available, pass in as
        keyword arguments foo="bar", foobar="", bar=foo 
        test input keys against meta_data dict, return
        true, assign data to key if not empty
        """
        for arg in kwargs:
            if arg in self.meta_data.keys():
                print("arg=<%s>" % arg)
                status = self.q_meta(key=arg, data=kwargs[arg], is_set=True)
                if not status: 
                    return False
        return True
    def timedata(self, **kwargs):
        """
        like metadata there's a lot of time data of which epoch is the 
        quickest and easiest to input and derive other time info. Only 
        use UTC for epoch unless you know exactly where you are. The rest 
        can be found in self.time_data
        """
        for arg in kwargs:
            if arg in self.time_data.keys():
                status = self.q_time(key=arg, data=kwargs[arg], is_set=True)
                if not status: 
                    return False
        return True
    # --- end collect ---
    
    # --- get data ---
    # 
    def query(self, key, store, data, is_set):
        """return or update dictionary data by type or F"""
        if key in store:    # can we update by key?
            if is_set:      # do we want to update?
                if data:    
                    store[key] = data # update
                    return True
                else:
                    return False
            else:
                return store[key] # get query
        else:
            return False
    def marshall(self, dtype, key, data="", is_set=False):
        """
        determine which store, query and return or update 
        data by type or F
        """
        result = False
        if dtype in self.dtypes:
            if dtype == 'body':
                if key in self.body_data:
                    result = self.query(key, self.body_data, data, is_set)
            elif dtype == 'file':
                if key in self.file_data:
                    result = self.query(key, self.file_data, data, is_set)
            elif dtype == 'image':
                if key in self.image_data:
                    result = self.query(key, self.image_data, data, is_set)
            elif dtype == 'time':
                if key in self.time_data:
                    result = self.query(key, self.time_data, data, is_set)
            elif dtype == 'meta':
                if key in self.meta_data:
                    result = self.query(key, self.meta_data, data, is_set)
            else:
                pass
        return result
    #---
    # convenience methods for marshall->query 
    #---
    def q_meta(self, key, data="", is_set=False):
        return self.marshall('meta', key, data, is_set)
    def q_file(self, key, data="", is_set=False):
        return self.marshall('file', key, data, is_set)
    def q_body(self, key, data="", is_set=False):
        return self.marshall('body', key, data, is_set)
    def q_image(self, key, data="", is_set=False):
        return self.marshall('image', key, data, is_set)
    def q_time(self, key, data="", is_set=False):
        return self.marshall('time', key, data, is_set)
    # --- end get data ---
    
    # --- render ---
    #
    # template
    def build_template(self, template, data):
        """
        given template and data, return 
        substituted string with data
        """
        if template: # has template?
            if data: # has data?
                data_rendered = []
                data_raw = template.split('\n')
                for line in data_raw:
                    t = Template(line)
                    render = str(t.substitute(data))
                    data_rendered.append(render)
                return data_rendered
        return False
    # --- render ---
    # page
    def render_header(self):
        """
        given header data and template, substitute data for placeholders
        """
        # remember: the dict keys are related to <header.html> 
        #           key holders in the template
        print("0 site_name=<%s>" % self.q_meta('site_name'))
        print("0 site_byline=<%s>" % self.q_meta('site_byline'))
        print("0 site_domain=<%s>" % self.q_meta('site_domain'))

        header_map = dict(author=self.q_meta('author'),
                          site_name=self.q_meta('site_name'),
                          site_byline=self.q_meta('site_byline'),
                          site_domain=self.q_meta('site_domain'),
                          respath=self.q_file('respath'), 
                          title=self.q_body('title'),
                          abstract=self.q_body('abstract'), 
                          year=self.q_time('year'),
                          month_mmm=self.q_time('month_mmm'),
                          month_mm=self.q_time('month_mm'),
                          day=self.q_time('day'),
                          tool=self.q_meta('tool'),
                          version=self.q_meta('version'))

        header = self.build_template(self.__header, header_map)
        return header
    def render_body(self):
        """
        given data and template, substitute data for placeholders
        """
        # remember: the dict keys are related to <content.html> 
        #           key holders in the template
        print("1 site_name=<%s>" % self.q_meta('site_name'))
        print("1 site_byline=<%s>" % self.q_meta('site_byline'))

        body_map = dict(title=self.q_body('title'),
                        author=self.q_body('author'),
                        site_name=self.q_meta('site_name'),
                        site_byline=self.q_meta('site_byline'),
                        abstract=self.q_body('abstract'), 
                        description=self.q_body('description'),
                        body=self.q_body('body'),
                        year=self.q_time('year'),
                        respath=self.q_file('respath'), 
                        month_mmm=self.q_time('month_mmm'),
                        month_mm=self.q_time('month_mm'),
                        day=self.q_time('day'), 
                        img_url=self.q_image('img_url'),
                        img_src=self.q_image('img_src'),
                        img_height=self.q_image('img_height'),
                        img_width=self.q_image('img_width'),
                        dt_strf=self.q_time('dt_strf'))

        # grab the template, pass in the map, spit out the 
        # final body content
        body = self.build_template(self.q_body('template'), body_map)
        return body
    def render_footer(self):
        """
        given footer data and template, substitute data for placeholders
        """
        footer_map = dict(respath=self.q_file('respath'))
        footer = self.build_template(self.__footer, footer_map)
        return footer
    # all
    def render(self):
        header = self.render_header()
        body = self.render_body()
        footer = self.render_footer()
        try:
            with open(self.q_file('fullpath'),'wt') as f:
                # header
                for line in header:
                    f.write(line)
                    f.write("\n")
                # body
                for line in body:
                    f.write(line)
                    f.write("\n")
                # footer
                for line in footer:
                    f.write(line)
                    f.write("\n")

            f.close()
        except:
            header = ""
            body = ""
            footer = ""
            return False
        else:
            return True
    # --- end render
#
# --- end Page object ---



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
