#!/usr/bin/python
__author__ = 'LN'
import os
import json
import commands

data = {}
tcp_list = []
port_list = []
command = "netstat -ntlp|grep tcp|awk '{print $4}'|awk -F':' '{print $NF}'| sort -nr| uniq"
str = commands.getoutput(command)
ports = str.split('\n')
for port in ports:
    port_dict = {}
    port_dict['{#TCP_PORT}'] = port
    tcp_list.append(port_dict)

data['data'] = tcp_list
jsonStr = json.dumps(data, sort_keys=True, indent=4)
print  jsonStr
