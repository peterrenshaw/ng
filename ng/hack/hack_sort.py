import time
import datetime

def dt_ymdhm2_epoch(year,month,day,hour,minute):
    """return datetime in UTC epoch format"""
    t = datetime.datetime(year,month,day,hour,minute)
    return time.mktime(t.timetuple())




"""
urls.append((dt_ymdhm2_epoch(year=2013,month=10,day=18,hour=0,minute=0),
              'Hello world #1','http://foo.com',2013,10,18,0,0))
urls.append((dt_ymdhm2_epoch(year=2013,month=10,day=2,hour=0,minute=0),
              'First post','http://foo.com/bar',2013,10,2,0,0))
urls.append((dt_ymdhm2_epoch(year=2013,month=10,day=23,hour=0,minute=0),
              'The latest post','http://foo.com/bar/foobar',2013,10,23,0,0))
urls.append((dt_ymdhm2_epoch(year=2013,month=10,day=29,hour=0,minute=0),
              'The very latest post','http://foo.com/bar/foobar',2013,11,29,0,0))
urls.append((dt_ymdhm2_epoch(year=2013,month=10,day=28,hour=0,minute=0),
              'Another post','http://foo.com/bar/foo',2013,11,28,0,0))
urls.append((dt_ymdhm2_epoch(year=2012,month=12,day=25,hour=0,minute=0),
              'testing','http://127.0.0.1',2012,12,25,0,0))
urls.append((dt_ymdhm2_epoch(year=2013,month=4,day=1,hour=0,minute=0),
               'Hello world #1','http://192.168.0.1',2013,4,1,0,0))
urls.append((dt_ymdhm2_epoch(year=2013,month=10,day=20,hour=0,minute=0),
              'First post #3','http://foo.com/bar/1',2013,10,20,0,0))
urls.append((dt_ymdhm2_epoch(year=2013,month=10,day=21,hour=0,minute=0),
              'Hello world #2','http://foo.com',2013,10,21,0,0))
"""
#for day in urls:
#    print(day[0],day[3],day[4],day[5],day[1])
#print("\n\n")


#for day in sorted(urls, key=lambda epoch: urls[0]):
#   print(day[0],day[3],day[4],day[5],day[1])




#sorted(student_objects, key=lambda student: student.age)
"""
class Student:
        def __init__(self, name, grade, age):
                self.name = name
                self.grade = grade
                self.age = age
        def __repr__(self):
                return repr((self.name, self.grade, self.age))
"""
class Links:
        def __init__(self, epoch, title, url, year, month, day):
            self.epoch = epoch
            self.title = title
            self.url = url
            self.year = year
            self.month = month
            self.day = day
            #self.hour = hour
            #self.minute = minute
        def __repr__(self):
            return repr((self.epoch,
                         self.title,
                         self.url,
                         self.year,
                         self.month,
                         self.day)) 

urls = []
urls.append(Links(epoch=dt_ymdhm2_epoch(year=2013,month=10,day=18,hour=0,minute=0),title='Hello world #1',url='http://192.168.0.1',year=2013,month=4,day=1))
urls.append(Links(epoch=dt_ymdhm2_epoch(year=2013,month=10,day=2,hour=0,minute=0),title='Hello world #2',url='http://foo.com',year=2013,month=10,day=21))
urls.append(Links(epoch=dt_ymdhm2_epoch(year=2013,month=10,day=23,hour=0,minute=0),title='First post',url='http://foo.com/bar',year=2013,month=10,day=2))
urls.append(Links(epoch=dt_ymdhm2_epoch(year=2013,month=10,day=29,hour=0,minute=0),title='The latest post',url='http://foo.com/bar/foobar',year=2013,month=10,day=23))
urls.append(Links(epoch=dt_ymdhm2_epoch(year=2013,month=10,day=28,hour=0,minute=0),title='The very latest post',url='http://foo.com/bar/foobar',year=2013,month=11,day=29))

posts = sorted(urls, key=lambda links: links.epoch)
for post in posts:
    print(post.epoch, post.year, post.month, post.day, post.title)
print(dt_ymdhm2_epoch(year=2013,month=10,day=18,hour=0,minute=0))
print(dt_ymdhm2_epoch(year=2013,month=10,day=28,hour=0,minute=0))
