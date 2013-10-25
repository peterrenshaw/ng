#!/usr/bin/env python
# ~*~ encoding: utf-8 ~*~


import os
import time
import datetime
from string import Template


# --- time tools ---
#
# dt_epoch_utc: epoch, utc
def dt_epoch_utc():
    """return datetime in UTC epoch format"""
    t = datetime.datetime.utcnow()
    return time.mktime(t.timetuple())
# dt_datetime_strf: format return using strf strings
def dt_datetime_strf(strf_format, is_upper=False):
    """datetime formatted using STRF string format"""
    dt = datetime.datetime.now().strftime(strf_format)
    if is_upper: dt = dt.upper()
    return dt
#
# --- end time tools ---






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
                              name="",        # filename
                              ext="",         # filename extension
                              fullpath="")    # full filepath and filename.ext
        # time
        self.time_data = dict(dt_epoch="",       # epoch
                              year="",        # year YYYY
                              month="",       # mmm or mm
                              mmm="",         # mmm == JAN, FEB, etc
                              mm="",          # mm == 01, 02, etc, zero pad
                              day="",         # 01, 02, etc zero pad
                              hour="",        # hour in HH format, zero pad
                              minute="",      # minute in MM fomat, zero pad
                              dt_strf="")     # string formatted date time
        # meta
        self.meta_data = dict(author="",              # author name
                              site_name="",           # name of site
                              site_byline="",         # site tag line
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
                               site="",
                               site_byline="",
                               title="",
                               abstract="", 
                               year="",
                               mmm="",
                               mm="",
                               day="",
                               tool="",
                               version="")
        # body
        self.body_map = dict(title="",
                             site="",
                             abstract="", 
                             description="",
                             body="",
                             year="",
                             mmm="",
                             mm="",
                             day="", 
                             img_url="",
                             img_src="",
                             img_height="",
                             img_width="",
                             dt_strf="")
        # index
        self.index_map = dict(title="",
                              abstract="",
                              file_path="",
                              year="",
                              mmm="",
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
                if self.q_file('relpath'):
                    fullpath = os.path.join(self.q_file('basepath'),
                                            self.q_file('relpath'), fn)
                else:
                    fullpath = os.path.join(self.q_file('basepath'), fn)
                return self.q_file('fullpath', data=fullpath, is_set=True)
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
        """determine which store, query and return or update data by type or F"""
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
        """given header data and template, substitute data for placeholders"""
        # remember: the dict keys are related to <header.html> 
        #           key holders in the template
        header_map = dict(author=self.q_meta('author'),
                          site=self.q_meta('site_name'),
                          site_byline=self.q_meta('site_byline'),
                          title=self.q_body('title'),
                          abstract=self.q_body('abstract'), 
                          year=self.q_time('year'),
                          mmm=self.q_time('mmm'),
                          mm=self.q_time('mm'),
                          day=self.q_time('day'),
                          tool=self.q_meta('tool'),
                          version=self.q_meta('version'))

        header = self.build_template(self.__header, header_map)
        return header
    def render_body(self):
        """given data and template, substitute data for placeholders"""
        # remember: the dict keys are related to <content.html> 
        #           key holders in the template
        body_map = dict(title=self.q_body('title'),
                        site_name=self.q_meta('site_name'),
                        abstract=self.q_body('abstract'), 
                        description=self.q_body('description'),
                        body=self.q_body('body'),
                        year=self.q_time('year'),
                        mmm=self.q_time('mmm'),
                        mm=self.q_time('mm'),
                        day=self.q_time('day'), 
                        img_url=self.q_image('img_url'),
                        img_src=self.q_image('img_src'),
                        img_height=self.q_image('img_height'),
                        img_width=self.q_image('img_width'),
                        dt_strf=self.q_time('dt_strf'))

        # grab the template, pass in the map, spit out the final body content
        body = self.build_template(self.q_body('template'), body_map)
        return body
    def render_footer(self):
        footer = "%s" % self.__footer
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
                if footer:
                    f.write(footer)
            f.close()
        except:
            header = ""
            body = ""
            footer = ""
            return False
        else:
            return True
    # --- end render


#---
# main:  
#---
def main():
    destination = 'E:\\blog\\seldomlogical'


    author = "Peter Renshaw" 
    site = "Seldomlogical"
    site_byline = "new ideas, ideal solutions are seldom logical. attaining a desired goal always is"
    title = "Hello world"
    abstract = "A quick hello world hack. Not much too look at but you have to start somewhere."
    img_url = "http://www.flickr.com/photos/bootload/7419372302/"
    img_src = "http://farm9.staticflickr.com/8154/7419372302_f34e56a94c.jpg"
    img_height = "375"
    img_width = "500"


    # "Thursday, 19 July 2012 09:41"
    str_full = "%A, %d %B %Y %H:%M"
    dt_full = dt_datetime_strf(str_full) 
    str_24hour = dt_datetime_strf("%H")
    str_minute = dt_datetime_strf("%M")
    dt_epoch = dt_epoch_utc()
    is_index=True

    header = ""
    hp = os.path.join(os.curdir, 'source', 'partials', 'header.html')
    with open(hp, encoding='utf-8') as f:
        header = f.read()
    f.close()

    footer = ""
    fp = os.path.join(os.curdir, 'source', 'partials', 'footer.html')
    with open(fp, encoding='utf-8') as f:
        footer = f.read()
    f.close()    

    tpl = ""
    tp = os.path.join(os.curdir, 'source', 'partials', 'content.html')
    with open(tp, encoding='utf-8') as f:
        tpl = f.read()
    f.close()

    content = ""
    cp = os.path.join(os.curdir, 'source', 'page.txt')
    with open(cp, encoding='utf-8') as f:
        content = f.read()
    f.close()


    p = Page(is_index)
    p.header(header)
    p.footer(footer)
    p.imagedata(source=img_src,
                url=img_url,
                height=img_height,
                width=img_width)
    p.timedata(year="2013",
               mm="10",
               mmm="OCT",
               day="17",
               dt_strf=dt_full,
               dt_epoch=dt_epoch,
               hour=str_24hour,
               minute=str_minute)
    p.filedata(basepath=destination,name="index", ext="html")
    p.metadata(tags=['tag1','tag2'],
               author=author,
               site_name=site,
               site_byline=site_byline)
    p.body(title=title, abstract=abstract, content=content,template=tpl)
    p.render()

#---
# main app entry point
#--- 
if __name__ == '__main__':
    main()


# vim: ff=unix:ts=4:sw=4:tw=78:noai:expandtab
