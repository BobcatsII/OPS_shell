#!/usr/bin/python

import sys
import subprocess
import json
import logging
import optparse
import tempfile
import os
import fcntl
import struct
import socket
import re


netname = os.popen("ls /sys/class/net |head -n1").read().strip('\n')

param1=sys.argv[1]
username = 'root'
password = 'dYKAMc9K'
param=len(sys.argv)-1

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR  
        struct.pack('256s', ifname[:15])
    )[20:24])

status={}
mongo_host = get_ip_address(netname)
mongo_bin=subprocess.Popen(''' which mongo 2>/dev/null||echo '/usr/local/mongodb/bin/mongo'  ''',shell=True,stdout=subprocess.PIPE).stdout.readline().strip()
command_line=mongo_bin + " " + mongo_host + "/admin" + " " + "-u" + username + " " + "-p" + password


if param == 2:
    param2=sys.argv[2]
    if param2 == mongo_host:
        status = subprocess.Popen(''' echo 'db.serverStatus().%s' | %s |sed -n '3p' ''' %(param1,command_line),shell=True,stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.readline().strip()
        if 'NumberLong' in status:
            status1 = re.sub('\D', "", status)
            print status1        
        elif status == 'true':
            print 1
        elif status == 'false':
            print 0
        else:            
            print status

elif param == 3:
    param2=sys.argv[2]
    param3=sys.argv[3]
    if param3 == mongo_host:
        status = subprocess.Popen(''' echo 'db.serverStatus().%s.%s' | %s | sed -n '3p' ''' %(param1,param2,command_line),shell=True,stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.readline().strip()
        if 'NumberLong' in status:
            status1 = re.sub('\D', "", status)
            print status1
        elif status == 'true':
            print 1
        elif status == 'false':
            print 0
        else:
            print status

elif param == 4:
    param2=sys.argv[2]
    param3=sys.argv[3]
    param4=sys.argv[4]
    if param4 == mongo_host:
        status=subprocess.Popen(''' echo 'db.serverStatus().%s.%s.%s' | %s | sed -n '3p' ''' %(param1,param2,param3,command_line),shell=True,stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.readline().strip()
        if 'NumberLong' in status:
            status1 = re.sub('\D', "", status)
            print status1
        elif status == 'true':
            print 1
        elif status == 'false':
            print 0
        else:
            print status
