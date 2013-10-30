#!/usr/bin/env python
# ~*~ encoding: utf-8 ~*~



#===
# name: Links
# date: 2013OCT24
# prog: pr
# desc: container to expose tuple of time for sorting
#===
class Link:
        def __init__(self, epoch, title, url, year, month, day, hour, minute):
            self.epoch = epoch
            self.title = title
            self.url = url
            self.year = year
            self.month = month
            self.day = day
            self.hour = hour
            self.minute = minute
        def __repr__(self):
            return repr((self.epoch,
                         self.title,
                         self.url,
                         self.year,
                         self.month,
                         self.day,
                         self.hour,
                         self.minute))

def main():
    urls = []
    urls.append(Link(epoch=dt_ymdhm2_epoch(year=2013,month=10,day=1,hour=0,minute=0),
                                        title='Hello world #1',url='http://192.168.0.1',
                                        year=2013,month=4, day=1, hour=0, minute=0))
    urls.append(Link(epoch=dt_ymdhm2_epoch(year=2013,month=10,day=21,hour=0,minute=0),
                                        title='Hello world #2',url='http://foo.com',
                                        year=2013,month=10,day=21, hour=0, minute=0))
    urls.append(Link(epoch=dt_ymdhm2_epoch(year=2013,month=10,day=2,hour=0,minute=0),
                                        title='First post',url='http://foo.com/bar',
                                        year=2013,month=10,day=2, hour=0, minute=0))
    urls.append(Link(epoch=dt_ymdhm2_epoch(year=2013,month=10,day=23,hour=0,minute=0),
                                        title='The latest post',url='http://foo.com/bar/foobar',
                                        year=2013,month=10,day=23, hour=0, minute=0))
    urls.append(Link(epoch=dt_ymdhm2_epoch(year=2013,month=10,day=29,hour=0,minute=0),
                                        title='The very latest post',url='http://foo.com/bar/foobar',
                                        year=2013,month=11,day=29,hour=0, minute=0))
    urls.append(Link(epoch=dt_ymdhm2_epoch(year=2011,month=5,day=22,hour=0,minute=0),
                                        title='Testing',url='http://foo.com/test',
                                        year=2011,month=5,day=22, hour=0, minute=0))
    urls.append(Link(epoch=dt_ymdhm2_epoch(year=1971,month=8,day=21,hour=0,minute=0),
                                        title='goo gaa',url='http://bbn.com',
                                        year=1971,month=8,day=21, hour=0, minute=0))
    print("needs sorting...")
    for url in urls:
        print(url.year, url.month, url.day, url.title)

    print("sorting...")
    posts = sorted(urls, key=lambda link: link.epoch, reverse=True)
    for post in posts:
        print(post.year, post.month, post.day, post.title)


#---
# main app entry point
#--- 
if __name__ == '__main__':
    main()


# vim: ff=unix:ts=4:sw=4:tw=78:noai:expandtab    
