#!/usr/bin/python
#-*- coding:utf-8 -*-

import os
import codecs
import datetime

"""
   每分钟统计一次指定人员的请求日志并存为文件，并从文件中分离出异常的日志存储到异常文件中去。
   #crontab -l
   * * * * *  python /your/path/count_tel.py
   #每日清理一次
   0 1 * * *  find /your/logs_path/leaders -mindepth 2 -maxdepth 2 -mtime +2 -type f -exec rm -rf {} \;
"""


def count_log(telph, filedir, now, accesslog):
    for name in telph.values():
        leaderdir = "{0}/{1}".format(filedir, name)
        if os.path.exists(leaderdir) is False:
            os.makedirs(leaderdir)
    for tel in telph.keys():
        leadername = telph[tel]
        tellog = "{0}/{1}/{2}_{3}_log.txt".format(filedir, leadername, now, tel)
        abormallog = "{0}/{1}/{2}_{3}_abormal_log.txt".format(filedir, leadername, now, tel)
        with codecs.open(accesslog, "r") as f:
            leaderlog = ''.join([x for x in f.readlines()[-50000:] if "{0}".format(tel) in x])
            print leaderlog
        with codecs.open(tellog, "a+") as w:
            w.write(leaderlog)
        with codecs.open(tellog, "r") as fr:
            tmplog = ''.join([y for y in fr.readlines() if "[200" != y.split(']')[10] and "[302" != y.split(']')[10]])
        with codecs.open(abormallog, "a+") as fw:
            fw.write(tmplog)

def main():
    leaders_telph = {
        "18xxxxxxxx9":"g**g",
        "17xxxxxxxx7":"w**i",
        "13xxxxxxxx2":"l**i",
        }
    filedir = "/data/Logs_Backup/leaders"
    now = datetime.datetime.now().strftime('%Y%m%d%H%M')
    accesslog = "/data/log/tysx/access.log"
    count_log(leaders_telph, filedir, now, accesslog)

if __name__ == "__main__":
    main()
