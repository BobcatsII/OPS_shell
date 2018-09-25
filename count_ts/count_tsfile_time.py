#!/usr/bin/python
#-*- coding:utf-8 -*- 

import os
import datetime
import threading
from helper import date_helper, str_helper, log_helper, sys_helper, mysql_helper, http_helper


def search_file(filepath, L):
    for fn in os.listdir(filepath):
        if minute in fn and 'ts.ts' not in fn:
            L.append(fn)
    return L

def execut_file(filepath, L):
    for f in search_file(filepath, L):
        cmd = "{0} -v quiet -print_format json -show_format -i {1}{2}".format(
		ffscpt, filepath, f)
        res = os.popen(cmd)
        infos = str_helper.json_decode(res.read().strip())
        if infos.get('format', None) is not None:
            du = infos['format']['duration']
            params = (f, du,)
            print params
            id = mysql_helper.insert_or_update_or_delete(sqlup, params, True)

def find_dir():
    cnlst = [ name for name in os.listdir(dirpath) if '512k' in name ]
    for cname in cnlst:
        filepath = "{0}/{1}/{2}/".format(dirpath, cname, today)
        print (filepath)
        isExists = os.path.exists(filepath)
        print (isExists)
        if isExists == "True":
            t = threading.Thread(target=execut_file, args=(filepath, L))
            t.start()
        else:
            print ("{0} dir no exists!".format(filepath))
            continue

if __name__ == '__main__':    
    #当天日期
    today = datetime.datetime.now().strftime("%Y%m%d")
    #上一分钟时间
    minute = (datetime.datetime.now()-datetime.timedelta(minutes=1)).strftime("%Y%m%d_%H%M")
    dirpath = "/data/ts"
    ffscpt = "/usr/bin/ffprobe"
    sqlup = '''INSERT INTO tmts (name, time) value (%s, %s)'''
    L = []
    find_dir()
