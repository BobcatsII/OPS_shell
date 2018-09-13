#!/usr/bin/python

import json
import logging
import os
import sys
import socket
import fcntl  
import struct 


netname = os.popen("ls /sys/class/net |head -n1").read().strip('\n')

def get_ip_address(ifname):  
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
    return socket.inet_ntoa(fcntl.ioctl(  
        s.fileno(),  
        0x8915,  # SIOCGIFADDR  
        struct.pack('256s', ifname[:15])  
    )[20:24])  

element = {'{#MONGO_HOST}': get_ip_address(netname)}
print json.dumps({"data": [element]})
