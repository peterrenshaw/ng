#!/usr/bin/env python
# ~*~ encoding: utf-8 ~*~


#===
# name: hack_sort3.py
# date: 2013OCT25
# prog: pr
# desc: funky Container class that lets you add dictionaries 
#       of data and sort them by key. 
# src : <http://docs.python.org/3.2/howto/sorting.html>
#===

import time
import datetime


#---
# dt_ymdhm2_epoch: pass in y/m/d/h:m spits out epoch
#---
def dt_ymdhm2_epoch(year,month,day,hour,minute): # TODO add optional seconds
    """return datetime in epoch format defined by y,m,d,h,m"""
    t = datetime.datetime(year,month,day,hour,minute)
    return time.mktime(t.timetuple())


#===
# name: Container
# date: 2013OCT24
# prog: pr
# desc: using only list and dictionary, sort the list of
#       dictionary values by key. The object allows you to 
#       add multiple dictionaries of data (test) then sort by 
#       existing key. 
#
#       funky :)
#===
class Container:
    def __init__(self):
        """initialise variables"""
        self.index = []
        self.data = {}
    def add(self, **kwargs):
        """
        enter multiple key=value items, convert to dict
        save to master index - clear dict for next add
        """
        self.data = {}
        for key in kwargs:
            self.data[key] = kwargs[key]
        self.index.append(self.data)
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
        self.data = {}
    def all(self):
        """all index data in list"""
        return self.index


# main cle enty point
def main():
    """main cli entry point"""
    
    c = Container()
    c.add(epoch=dt_ymdhm2_epoch(year=2013,month=10,day=1,hour=0,minute=0),
           title='Hello world #1',url='http://192.168.0.1',year=2013,month=4, 
           day=1, hour=0,minute=0)
    c.add(epoch=dt_ymdhm2_epoch(year=2013,month=10,day=21,hour=0,minute=0),
           title='Hello world #2',url='http://foo.com',year=2013,month=10,
           day=21, hour=0, minute=0)
    c.add(epoch=dt_ymdhm2_epoch(year=2013,month=10,day=2,hour=0,minute=0),
           title='First post',url='http://foo.com/bar',year=2013,month=10,
           day=2, hour=0, minute=0)
    c.add(epoch=dt_ymdhm2_epoch(year=2013,month=10,day=23,hour=0,minute=0),
           title='The latest post',url='http://foo.com/bar/foobar',year=2013,
           month=10,day=23, hour=0, minute=0)
    c.add(epoch=dt_ymdhm2_epoch(year=2013,month=10,day=29,hour=0,minute=0),
           title='The very latest post',url='http://foo.com/bar/foobar',
           year=2013,month=11,day=29,hour=0, minute=0)
    c.add(epoch=dt_ymdhm2_epoch(year=2011,month=5,day=22,hour=2,minute=10),
           title='Testing 1',url='http://foo.com/test',
           year=2011,month=5,day=22, hour=2, minute=10)
    c.add(epoch=dt_ymdhm2_epoch(year=2011,month=5,day=22,hour=22,minute=43),
           title='Testing 2',url='http://foo.com/test',
           year=2011,month=5,day=22, hour=22, minute=43)
    c.add(epoch=dt_ymdhm2_epoch(year=1971,month=8,day=21,hour=0,minute=0),
           title='goo gaa',url='http://bbn.com',
           year=1971,month=8,day=21, hour=0, minute=0)

    # sort by time, epoch is dirty hack to ensure
    # datetime is sorted correctly
    print("sort by epoch")
    for p in c.sort('epoch'):
        print(p['epoch'],p['year'],p['month'],p['day'],p['hour'],p['title'])
    print("\n")

    # reverse date
    print("sort by epoch, reverse")
    for p in c.sort('epoch', order=False):
        print(p['epoch'],p['year'],p['month'],p['day'],p['hour'],p['title'])
    print("\n")

    # sort by title  TODO 'f' before 'g' ???
    print("sort by title")
    for p in c.sort('title'):
        print(p['epoch'],p['year'],p['month'],p['day'],p['hour'],p['title'])


#---
# main app entry point
#--- 
if __name__ == '__main__':
    main()


# vim: ff=unix:ts=4:sw=4:tw=78:noai:expandtab
