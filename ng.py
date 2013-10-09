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
import os.path
from optparse import OptionParser


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
        self.destination_dir = ""
        self.ext = ["md","markdown","txt"]
        self.filepath = []
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
            self.destination_dir = fdp
            return True
        else:
            return False
    # filepaths
    def file_paths(self):
        """return list of filepaths or F"""
        if len(self.filepath) > 0: return self.filepath
        else: return False
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
                fpn =  [os.path.realpath(f) for f in glob.glob(gfp)]
                if fpn: 
                    self.filepath = fpn

            if self.filepath:
                return True

        return False
    # processing
    def process(self):
        """process source files into datastructure"""
        pass



# main entry point
def main():
    usage = "usage: %prog [v] -s -d"
    parser = OptionParser(usage)

    # --- options --- 
    parser.add_option("-s", "--source", dest="source_directory",
                      help="supply source directory to read files from")
    parser.add_option("-d", "--destination", dest="destination_directory", 
                      help="supply destination directory to save files too")
    parser.add_option("-v", "--version", dest="version",
                      action="store_true",
                      help="current version")    
    options, args = parser.parse_args()

    # --- process ---
    if options.source_directory:
        if os.path.isdir(options.source_directory):
            print("source <%s>" % options.source_directory)
            if options.destination_directory:
                if os.path.isdir(options.destination_directory):
                    
                    # the business
                    ng = Nextgen()
                    ng.source(options.source_directory)
                    ng.read()
                    p = ng.file_paths()
                    for f in p:
                        print("\t%s" % f)
                    print("destination <%s>" % options.destination_directory)
                else:
                    print("error: must supply a valid <destination directory>")
                    print("\t<%s>" % options.destination_directory)
                    sys.exit(1)
            else:
                    parser.print_help()
                    print("\nerror: must supply a <destination directory>")
                    sys.exit(1)                
        else:
            print("error: must supply a valid <source directory>")
            print("\t<%s>" % options.source_directory)
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
