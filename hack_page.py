#!/usr/bin/env python
# ~*~ encoding: utf-8 ~*~


import os
import string
from string import Template


class Page:
    def __init__(self, is_index):
        """initialise the Page"""
        # basic page
        self.__header = ""     # template
        self.__footer = ""     # template
        self.__body = ""       # container for body
                         
        # body data
        self.body_data = dict(title="",    # title, 40 char limit
                              abstract="", # 120 char summary
                              summary="",  # 100 word summary
                              content=[])  # list of content
        # file data
        self.file_data = dict(path="",     # valid, relative fp to basepath
                              name="",
                              ext="",
                              filepathname="")      # path/filename.ext as url !filesys
        # meta data
        self.meta_data = dict(author="",
                              tags=[],
                              date="",
                              year="",
                              month="",
                              mmm="",
                              mm="",
                              day="",
                              is_index=(True if is_index else False))
                         
    # --- collect data ---
    #
    def header(self, content):
        """html/text template for header"""
        if content:
            self.__header = content
            return True
        return False
    def body(self, title, abstract, content):
        """body of page"""
        status = False
        if title:
            if abstract:
                if content:
                    self.body_data['title'] = title
                    self.body_data['abstract'] = abstract
                    self.body_data['content'] = content
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
        if dtype in ['meta','file','body']:
            if dtype == 'meta':
                if key in self.meta_data:
                    data = self.meta_data[key]
            elif dtype == 'file':
                if key in self.file_data:
                    data = self.file_data[key]
            elif dtype == 'body':
                if key in self.body_data:
                    data = self.body_data[key]
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
        if not self.get_meta('is_index'):
            # normal content page
            #

            # build header
            header_map = dict(author=self.get_meta('author'),
                              title=self.get_body('title'),
                              abstract=self.get_body('abstract'), 
                              year=self.get_meta('year'),
                              mmm=self.get_meta('mmm'),
                              day=self.get_meta('day'))
            header = self.build_template(self.__header, header_map)
            
            # build content
            # assuming no templating in content
            content = self.get_body('content')

            # build footer
            # assuming no templating in footer
            footer = "%s" % self.__footer

            try:
                print("writing to <%s>" % self.get_file('filepathname'))
                with open(self.get_file('filepathname'),'wt') as f:
                    for line in header:
                        f.write("%s\n" % line)
                    if content:
                        f.write(content)
                    if footer:
                        f.write(footer)
                    print("written")
                    f.close()
            except:
                data = ""
                if f: f.close()
                return False
            else:
                return True
        else:
            # index page
            pass
    # --- render ---


def main():
    destination = 'E:\\blog\\seldomlogical'

    h = ""
    hp = os.path.join(os.curdir, 'source', 'partials', 'header.html')
    with open(hp, encoding='utf-8') as f:
        h = f.read()
    

    ft = ""
    fp = os.path.join(os.curdir, 'source', 'partials', 'footer.html')
    with open(fp, encoding='utf-8') as f:
        ft = f.read()
   
    c = ""
    cp = os.path.join(os.curdir, 'source', 'page.txt')
    with open(cp, encoding='utf-8') as f:
        c = f.read()

    t = "Hello world"
    a = "A quick hello world hack. Not much too look at but you have to start somewhere."
    is_index=False

    p = Page(is_index)
    p.header(h)
    p.footer(ft)
    if p.body(title=t, abstract=a, content=c):
        if p.filename(path=destination, name="PAGE", ext="html"):
            if p.metadata(tags=['tag1','tag2'],author="peterrenshaw",
                          year="2013",mm="10",mmm="OCT",day="17"):
                if p.render():
                    print("ok")

#---
# main app entry point
#--- 
if __name__ == '__main__':
    main()


# vim: ff=unix:ts=4:sw=4:tw=78:noai:expandtab
