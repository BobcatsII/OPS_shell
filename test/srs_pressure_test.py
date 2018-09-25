#!/usr/bin/python
#-*- coding:utf-8 -*-
#eg:
#                                           host          port   channel        m3u8  ts
#python /opt/scripts/other/linan/srstest.py 172.18.250.23 11080  TVcibnteadj01  20    1000
#取到完整ts的时间：/tmp/srs_getcomplete_tstime.txt
#获取到相关频道的m3u8日志文件：/tmp/srs_m3u8_{channel}.log
#指定m3u8个数的日志文件：/tmp/srs_m3u8_{channel}_ol.log
#m3u8平均响应时间文件：/tmp/srs_m3u8_avg.log
#m3u8响应>3s的文件：/tmp/srs_m3u8_avg_3s.log
#m3u8响应>6s的文件：/tmp/srs_m3u8_avg_6s.log


import os
import re
import sys
import time
import glob
import shutil
import urllib
import urllib2
import threading
from threading import current_thread

def exeTime(func): 
        def newFunc(*args, **args2):  
            t0 = time.time()  
            back = func(*args, **args2)  
            with open("/tmp/srs_getcomplete_tstime_{0}.txt".format(channel), 'a') as fg:
                fg.write("%.3f\n" % (time.time() - t0)) 
            return back  
        return newFunc

def m3u8log():
     os.popen("tail -1000000 /data/log/tysx/access.log|grep {0}|grep '\.m3u8'  >  /tmp/srs_m3u8_{1}.log".format(channel,channel))
     raw = os.popen("cat /tmp/srs_m3u8_{0}.log|wc -l".format(channel))
     a = raw.read().strip('\n')
     if m3u8_number < int(a):
         os.popen("cat /tmp/srs_m3u8_{0}.log |head -{1} > /tmp/srs_m3u8_{2}_ol.log".format(channel, m3u8_number, channel))
     else:
         os.popen("cat /tmp/srs_m3u8_{0}.log > /tmp/srs_m3u8_{1}_ol.log".format(channel, channel))


def m3u8res():
     with open("/tmp/srs_m3u8_{0}_ol.log".format(channel), 'r') as f:
         loglst = f.readlines()
         l1 = []
         for line in loglst:
             b = re.findall(r'\[(\d\.\d\d\d)', line)
             l1.append(b[0])
         l2 = [ float(x) for x in l1 ]
         if len(l2):
             avg = sum(l2)/len(l2) 
             with open('/tmp/srs_m3u8_avg.log', 'w') as fw:
                fw.write(time.strftime('%Y-%m-%dT%H:%M:%S',time.localtime(time.time())))
                fw.write("\nm3u8的平均响应时间: ")
                fw.write(str(avg))
         else:
             print ("没有获取到数据")
             sys.exit(1)
         l3 = []
         for num in l1:
             if float(num) > 3:
                 l3.append(num)
         os.popen("echo 'm3u8响应大于3s的占比:{0}' >> /tmp/srs_m3u8_avg_3s.log".format(len(l3)/len(l1)))
         l4 = []
         for num in l1:
             if float(num) > 6:
                 l4.append(num)
         os.popen("echo 'm3u8响应大于6s的占比:{0}' >> /tmp/srs_m3u8_avg_6s.log".format(len(l4)/len(l1)))


@exeTime
def tsDownTime(tsurl, localTs):
    urllib.urlretrieve(tsurl, localTs)

def m3u8thread(lst, ts_number):
    for ul in lst:
        url = "http://{0}:{1}{2}".format(host, port, ul)
        req  = urllib2.Request(url)
        res  = urllib2.urlopen(req)
        info = res.readlines()
        localDir = "/data/downTs/"
        if os.path.isdir(localDir):
            pass
        else:
            os.mkdir(localDir)
        urlList = []
        for eachline in info:
            line = eachline.strip('\n')
            if re.match('.*ts.*' ,line):
                urlList.append(line) 
        for everyURL in urlList:
            tsname = re.findall('TV.*ts', everyURL)
            localTs = localDir + tsname[0]
            tsurl = "http://{0}:{1}/slive/".format(host, port) + everyURL
            for k in xrange(int(ts_number)):
                t = threading.Thread(target=tsDownTime, args=(tsurl, localTs)) 
                t.start()
            thread2.append(t)
        print ("\033[1;32;40m当前ts线程数为: {0}\033[0m".format(len(thread2)))
        time.sleep(3)

if __name__ == '__main__':
    host = sys.argv[1]
    port = sys.argv[2]
    channel = sys.argv[3]
    m3u8_number = sys.argv[4]
    ts_number = sys.argv[5]
    threads = []
    thread2 = []
    m3u8log()
    m3u8res()
    with open('/tmp/srs_m3u8_{0}_ol.log'.format(channel),'r') as fu:
        urllst = fu.readlines()
        lst = []
        for i in urllst:
            c = re.findall(r'.*\[(.*)\]\[2',i)
            lst.append(c[0])
        for j in xrange(int(m3u8_number)):
            m = threading.Thread(target=m3u8thread, args=(lst,ts_number))
            #threads.append(m)
            if int(m3u8_number) > threading.active_count():
                m.start()
                print ("当前运行的m3u8的线程数为: {0}".format(threading.active_count()))
            else:
                sys.exit(1)
