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
                         
        # body data
        self.body_data = dict(title="",    # title, 40 char limit
                              abstract="", # 120 char summary
                              summary="",  # 100 word summary
                              content=[])  # list of content
        # file data
        self.file_data = dict(path="",     # valid, relative fp to basepath
                              name="",
                              ext="",
                              fpn="")      # path/filename.ext as url !filesys
        # meta data
        self.meta_data = dict(tags=[],
                              date="",
                              year="",
                              month="",
                              mmm="",
                              mm="",
                              day="",
                              is_index=False)
                         
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
            #self.title = title
            self.body_data['title'] = title
            if abstract:
                #self.abstract = abstract
                self.body_data['abstract'] = abstract
                if content: 
                    #self.content = content # optional content
                    self.body_data['content'] = content
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
        status = False
        if os.path.isdir(path):
            if ext in ['html', 'htm']:
                if name:
                    self.file_data['path'] = path
                    self.file_data['ext'] = ext
                    self.file_data['name'] = "%s.%s" % (name, ext)
                    self.file_data['fpn'] = "%s/%s" % (self.file_data['path'], 
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
        return self.get('fire', key)
    def get_body(self, key):
        """return body_data by key or F"""
        return self.get('body', key)
    # --- end call data
    # --- build ---
    def build(self):
        """"build a page from bits of data"""
        # index page OR content page
        
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
