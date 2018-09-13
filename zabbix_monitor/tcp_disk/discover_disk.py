#!/usr/bin/python
__author__ = 'LN'
import os
import json
import commands

data = {}
disk_list = []
command = "cat /proc/diskstats |grep -E 'sd[a-z] |xvd[a-z] |vd[a-z] '|awk '{print $3}'|sort|uniq  2>/dev/null"
str = commands.getoutput(command)
disks = str.split('\n')
for disk in disks:
    disk_dict = {} 
    disk_dict['{#DISK_NAME}'] = disk
    disk_list.append(disk_dict)
data['data'] = disk_list
jsonStr = json.dumps(data, sort_keys=True, indent=4)
print  jsonStr
