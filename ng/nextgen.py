#! /usr/bin/env python3.3
# ~*~ encoding: utf-8 ~*~


#===
# name: nextgen.py
# date: 2013OCT09
# prog: pr
# desc: quick hack for a not so nextgen 
#       static html site generator
# use : nextgen.py -s <source> -d <dest>
#===


import os
import sys
from optparse import OptionParser


import ng
from ng.site import Nextgen
from ng.tools import DateIso8601


# main entry point
def main():
    usage = "usage: %prog [v] -s -d"
    parser = OptionParser(usage)

    # --- options --- 
    parser.add_option("-s", "--source", dest="source",
                      help="supply source directory to read files from")
    parser.add_option("-d", "--destination", dest="destination", 
                      help="supply destination directory to save files too")
    parser.add_option("-v", "--version", dest="version",
                      action="store_true",
                      help="current version")    
    options, args = parser.parse_args()

    # --- version ---
    if options.version:
       print("%s %s" % ("nextgen", "0.1"))
       sys.exit(0)

    # --- process ---
    read = False
    process = False
    save = False

    # source
    if options.source:
        if os.path.isdir(options.source):
            print("source <%s>" % options.source)
        
            dt = DateIso8601("")
            ng = Nextgen(dt)

            read = ng.read(options.source)
            if read:
                for f in ng.filepath:
                    print("\t%s" % f)
            
            # destination
            if options.destination:
                if os.path.isdir(options.destination):
                    print("destination <%s>" % options.destination)
              
                    # process
                    process = ng.process(options.destination)
                    if process:
                        print("process")
                        print("index")
                        for index in ng.index:
                            print("%s" % index.body_data)
                            print("%s" % index.time_data)
                            print("%s" % index.file_data)
                            print("%s" % index.meta_data)
                            print("\n")

                        print("post")
                        #for post in ng.post:
                        #    for key in post.keys():
                        #        print("\t%s" % key)
                        save = ng.save()
                        if save:
                            print("save")
                            sys.exit(1)
    
    if not (options.source and options.destination and read and process and save):
        parser.print_help()
        print("\n")
        print("Error: Houston, we *some* have problems")
        print("\tsource path <%s>" % options.source)
        print("\tng.source is %s" % (os.path.isdir(options.source) if options.source else False))
        print("\tdestination path <%s>" % options.destination)
        print("\tng.destination is %s" % (os.path.isdir(options.destination) if options.destination else False))
        print("\tng.read is %s" % read)
        print("\tng.process is %s" % process)
        print("\tng.save is %s" % save)


#---
# main app entry point
#--- 
if __name__ == '__main__':
    main()


# vim: ff=unix:ts=4:sw=4:tw=78:noai:expandtab
