#!/usr/bin/env python
# ~*~ encoding: utf-8 ~*~


import os
import time
import string
import datetime
from string import Template


def db_datetime_utc():
    """store datetime in UTC epoch format"""
    t = datetime.datetime.utcnow()
    return time.mktime(t.timetuple())
def dt_datetime_strf(strf_fmt, is_upper=False):
    dt = datetime.datetime.now().strftime(strf_fmt)
    if is_upper: dt = dt.upper()
    return dt

class Page:
    def __init__(self, is_index):
        """initialise the Page"""
        self.is_index = (True if is_index else False)
        self.index = []

        # basic page
        self.__header = ""     # template
        self.__footer = ""     # template
        self.__body = ""       # container for body
                         
        # body data
        self.body_data = dict(title="",     # title, 40 char limit
                              abstract="",  # 120 char summary
                              summary="",   # 100 word summary
                              content="",   # list of content
                              template="")  # template
        # file data
        self.file_data = dict(basepath="",
                              path="",     # valid, relative fp to basepath
                              name="",
                              ext="",
                              filepathname="") # path/filename.ext as url !filesys

        # tool data
        self.tool_data = dict(tool="nextgen.ng",
                              version="0.1")

        # meta data
        self.meta_data = dict(author="",    # author
                              site="",      # site name
                              site_byline="", # site tagline 
                              tags=[],      # tags as list
                              epoch="",
                              date="",      # date in dt format
                              year="",      # yyyy
                              month="",     # mmm or mm
                              mmm="",       # mmm = JAN,FEB etc
                              mm="",        # mm = 01,02 etc zero padded
                              day="",       # 01,02 etc zero padded
                              hour="",      # hour in HH format
                              minute="",    # minute in MM format
                              dt_format="", # date in string format
                              dt_epoch="",  # date in epoch format
                              img_url="",   # url to image
                              img_src="",   # source path to image
                              img_height="",# height image
                              img_width="", # width image
                              is_index=self.is_index)
                         
    # --- collect data ---
    #
    def header(self, content):
        """html/text template for header"""
        if content:
            self.__header = content
            return True
        return False
    def body(self, title, abstract, content, template):
        """body of page"""
        status = False
        if title:
            if abstract:
                if content:
                    if template: 
                        self.body_data['title'] = title
                        self.body_data['abstract'] = abstract
                        self.body_data['content'] = content
                        self.body_data['template'] = template
                        status = True # all ok, else fail
        return status
    def footer(self, content):
        """html/text template for footer"""
        if content:
            self.__footer = content
            return True
        return False
    def filename(self, path, name, ext):
        """build page filename with path, name and ext"""
        status = False
        if os.path.isdir(path):
            if ext in ['html', 'htm']:
                if name:
                    self.file_data['path'] = path
                    self.file_data['ext'] = ext
                    self.file_data['name'] = "%s.%s" % (name, ext)
                    self.file_data['filepathname'] = "%s/%s" % (self.file_data['path'], 
                                                                self.file_data['name'])
                    status = True
        return status
    def metadata(self, **kwargs):
        """
        lots of metadata available, pass in as
        keyword arguments foo="bar", foobar="", bar=foo 
        test input keys against meta_data dict, return
        true, assign data to key if not empty
        """
        status = False
        for arg in kwargs:
            if arg in self.meta_data.keys():
                if kwargs[arg]:
                    self.meta_data[arg] = kwargs[arg]
                    status = True
        return status
    #
    # --- end collect data ---
    # --- call data
    def get(self, dtype, key):
        """return data in data by type or F"""
        data = False
        if dtype in ['meta','file','body','tool']:
            if dtype == 'meta':
                if key in self.meta_data:
                    data = self.meta_data[key]
            elif dtype == 'file':
                if key in self.file_data:
                    data = self.file_data[key]
            elif dtype == 'body':
                if key in self.body_data:
                    data = self.body_data[key]
            elif dtype == 'tool':
                if key in self.tool_data:
                    data = self.tool_data[key]
            else:
                pass
        return data
    def get_meta(self, key):
        """return meta_data by key or F"""
        return self.get('meta', key)
    def get_file(self, key):
        """return file_data by key or F"""
        return self.get('file', key)
    def get_body(self, key):
        """return body_data by key or F"""
        return self.get('body', key)
    def get_tool(self, key):
        """return tool_data by key or F"""
        return self.get('tool', key)
    # --- end call data
    def build_template(self, template, data):
        """given template and data, return substituted str"""
        # TODO:  no testing here
        data_rendered = []
        data_raw = template.split("\n")
        for line in data_raw:
            t = string.Template(line)
            render = str(t.substitute(data))
            data_rendered.append(render)
        return  data_rendered
    # --- render ---
    def render(self):
        """"build a page from bits of data"""
        # index page OR content page
        print("is_index=%s" % self.get_meta('is_index'))
        if not self.get_meta('is_index'):
            # normal content page
            # build header
            header_map = dict(author=self.get_meta('author'),
                              site=self.get_meta('site'),
                              site_byline=self.get_meta('site_byline'),
                              title=self.get_body('title'),
                              abstract=self.get_body('abstract'), 
                              year=self.get_meta('year'),
                              mmm=self.get_meta('mmm'),
                              mm=self.get_meta('mm'),
                              day=self.get_meta('day'),
                              tool=self.get_tool('tool'),
                              version=self.get_tool('version'))
            header = self.build_template(self.__header, header_map)
            
            # build content
            content_map = dict(title=self.get_body('title'),
                               site=self.get_meta('site'),
                               abstract=self.get_body('abstract'), 
                               description=self.get_body('description'),
                               body=self.get_body('content'),
                               year=self.get_meta('year'),
                               mmm=self.get_meta('mmm'),
                               mm=self.get_meta('mm'),
                               day=self.get_meta('day'), 
                               img_url=self.get_meta('img_url'),
                               img_src=self.get_meta('img_src'),
                               img_height=self.get_meta('img_height'),
                               img_width=self.get_meta('img_width'),
                               dt_format=self.get_meta('dt_format'))
            contents = self.build_template(self.get_body('template'), content_map)
            
            # build footer
            # assuming no templating in footer
            footer = "%s" % self.__footer

            try:
                #print("writing to <%s>" % self.get_file('filepathname'))
                with open(self.get_file('filepathname'),'wt') as f:
                    for line in header:
                        f.write("%s\n" % line)
                    if contents:
                        for line in contents:
                             f.write(line)
                    if footer:
                        f.write(footer)
                f.close()
            except:
                data = ""
                if f: f.close()
                return False
            else:
                return True
        else:
            # index page
            fp = os.path.join(self.get_file('basepath'),
                              self.get_meta('year'), 
                              self.get_meta('mmm'),
                              self.get_meta('day'),
                              self.get_file('name'))
            link_map = dict(title=self.get_body('title'),
                            abstract=self.get_body('abstract'),
                            file_path=fp,
                            year=self.get_meta('year'),
                            mmm=self.get_meta('mmm'),
                            day=self.get_meta('day'),
                            dt_format=self.get_meta('dt_format'),
                            dt_epoch=self.get_meta('dt_epoch'),
                            hour=self.get_meta('hour'),
                            minute=self.get_meta('minute'))

            # call list of link data
            # sorted by?
            self.index.sort()
            print(link_map)
            print("len=%s" % len(self.index))
            for link in self.index:
                print(link, fp)
                #try:
                #print("writing to <%s>" % self.get_file('filepathname'))
                #    with open(self.get_file(fp),'wt') as f:
                #        pass
                #f.close()
                #except:
                #    if f: f.close()
                
            #     open file to write
            #         title = index.html
            #         path = yyyy/mmm/dd
            #         write index_link
            return True
    # --- render ---


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
    dt_epoch = db_datetime_utc()
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
    if p.body(title=title, abstract=abstract, content=content, template=tpl):
        if p.filename(path=destination, name="index", ext="html"):
            if p.metadata(tags=['tag1','tag2'],
                          author=author,
                          site=site,
                          site_byline=site_byline,
                          year="2013",mm="10",mmm="OCT",day="17",
                          img_url=img_url, 
                          img_src=img_src,
                          img_height=img_height, 
                          img_width=img_width,
                          dt_format=dt_full,
                          dt_epoch=dt_epoch,
                          hour=str_24hour,
                          minute=str_minute,
                          relpath=destination):
                if p.render():
                    print("ok")
                else:
                    print("bugger")

#---
# main app entry point
#--- 
if __name__ == '__main__':
    main()


# vim: ff=unix:ts=4:sw=4:tw=78:noai:expandtab
