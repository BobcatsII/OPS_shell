#!/usr/bin/env python
import os,commands
import json
#import simplejson as json

zk_pids=commands.getoutput("ps aux|grep zookeeper|grep -v grep |awk '{print $2}'")

ports = []

for zk_pid in zk_pids.split():
    t=os.popen("""netstat -tlpn |grep %s |awk '{print $4}'|awk -F: '{print $NF}'|sort |head -n1"""%(zk_pid))
    for port in  t.readlines():
        r = os.path.basename(port.strip())
        ports += [{'{#ZKPORT}':r}]
print json.dumps({'data':ports},sort_keys=True,indent=4,separators=(',',':'))
