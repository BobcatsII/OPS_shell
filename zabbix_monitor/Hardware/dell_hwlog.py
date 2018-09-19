#!/usr/bin/python
#coding:utf8

"""
  zabbix硬件监控（仅接受dell服务器）
  操作步骤：
    1.OMSA的先决包安装(如果需要)
      $ sudo yum install -y libxslt  （如果需要，则加上：net-snmp-utils setserial perl-libwww-perl）

    2.进入RPM包目录执行安装，自己拉出来只用于监控的omsz.zip包，解压
      $ cd /srvadmin      
      $ sudo rpm -ivh *
    3.进入dell目录,启动程序获取日志
      $ sudo /opt/dell/srvadmin/sbin/srvadmin-services.sh start
      
    4.监控脚本
"""

import os
import linecache
import time
from commands import *

date_time = time.strftime("%a %b %e")
cmd = getoutput("sudo /opt/dell/srvadmin/sbin/omreport system esmlog > /tmp/dell_hwlog.txt")

with open('/tmp/dell_hwlog.txt','r') as f:
    length = len(f.readlines())

for i in range(1,length):
    b=linecache.getline('/tmp/dell_hwlog.txt',i)
    if date_time in b:
        a=linecache.getline('/tmp/dell_hwlog.txt',i-1)
        c=linecache.getline('/tmp/dell_hwlog.txt',i+1)
        if 'Ok' not in a:
            cmd2 = getoutput(""" echo '%s' | awk -F':' '{print $2}' """ % c)
            print cmd2,
            
            
            
