#!/usr/bin/env python
# ~*~ encoding: utf-8 ~*~


import os


class Page:
    def __init__(self):
        """initialise the Page"""
        # basic page
        self.__header = ""     # template
        self.__footer = ""     # template
        self.__body = ""       # container for body

        # body
        self.title = ""      # display as is
        self.abstract = ""   # 120 char summary
        self.summary = ""    # 100 word summary
        self.content = []

        # filepath name 
        self.path = ""       # valid, relative filepath to basepath
        self.file_name = ""
        self.ext = ""
        self.fnp = ""        # 'path/filename.ext' as URL not filesys

        # metadata
        self.metadata = dict(tags=[],
                             date="",
                             year="",
                             month="",
                             mmm="",
                             mm="",
                             day="")
        self.tags = []       # tag data as list
        self.date = ""       # date as object
        self.year = ""       # yyyy
        self.month = ""      # month, [mmm|mm]
        self.mmm = ""        # month mmm, UC
        self.mm = ""         # month mm, string, 0 padding
        self.day = ""        # day, dd, string, 0 padding
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
        if title:
            self.title = title
            if abstract:
                self.abstract = abstract
                if content: 
                    self.content = content # optional content
                    return True # all ok, else fail
        return False
    def footer(self, content):
        """html/text template for footer"""
        if content:
            self.__footer = content
            return True
        return False
    def filename(self, path, name, ext):
        """build page filename with path, name and ext"""
        if os.path.isdir(path):
            self.path = path
            if ext in ['html', 'htm']:
                if name:
                    self.file_name = "%s.%s" % (name, ext)
                    self.fpn = "%s/%s" % (self.path, self.file_name)
                    return True
        return False
    def metadata(self, **kwargs):
        """
        lots of metadata available, pass in as
        keyword arguments
        """
        if kwargs.key in self.metadata.keys():
            for arg in kwargs:
                    self.metadata[arg.key] = arg.value
            return True
        return False
    # --- end collect data ---
    # --- build ---
    def build(self):
        """"build a page from bits of data"""
        pass
    # --- show ---
    def render(self):
        """render page, save as file"""
        pass 


def main():
    pass

#---
# main app entry point
#--- 
if __name__ == '__main__':
    main()


# vim: ff=unix:ts=4:sw=4:tw=78:noai:expandtab
