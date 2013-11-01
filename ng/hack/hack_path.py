#!/usr/bin/env python
# ~*~ encoding: utf-8 ~*~

#===
# name: hack_path.py
# date: 2013NOV01
# prog: pr
# desc: require a function that builds dynamically the
#       path back to root for resources.
#
#          cf: root = "."
#              file = /2013/OCT/31
#              resp = ..\..\..\
#
#       this allows the *file* point back to root
#       resources, css, images etc.
#===


import os
import os.path


#---
# build_respath: from path calc seps & return
#                path back to root.
#---
def build_respath(path, sep=os.path.sep, bw=".."):
    """
    build the resource path back to root and returns
    resource data or F
    """
    # check for os.path.altsep in path & die
    # as it gives unpredictable result
    if not path.count(os.path.altsep) > 0:
        if path: 
            resdata = ""
            # because counting b/w path
            count = path.count(sep) + 1
            for c in range(0, count):
                resdata = "%s%s%s" % (resdata, bw, sep)
            return resdata
    return False

# main: cli entry point
def main():

    # basic tests
    path7 = "%s%s" % (os.path.join("2013","JAN","21"), os.path.altsep)
    path6 = "/"
    path5 = ""
    path4 = os.path.join("2013","NOV","21")
    path3 = os.path.join("2013","10","30")
    path2 = os.path.join("2013","OCT")
    path1 = "."
    path0 = "\\"
    paths = [path0, path1, path2, path3,
             path4, path5, path6, path7]

    # loop thru paths for tests
    count = 0
    for p in paths:
        print("%s path=<%s> resdata=<%s>" % (count, p, build_respath(p)))
        count += 1


#---
# main app entry point
#--- 
if __name__ == '__main__':
    main()


# vim: ff=unix:ts=4:sw=4:tw=78:noai:expandtab
