import os
import commands
import json
                
redis_pids=commands.getoutput("ps aux|grep redis-server| grep -v sentinel|grep -v grep |awk '{print $2}'")
ports = []
for redis_pid in redis_pids.split():
    t=os.popen("""netstat -tlpn |grep %s |awk '{print $4}'|awk -F: '{print $NF}' |uniq"""%(redis_pid))
    for port in  t.readlines():
    r = os.path.basename(port.strip())
    ports += [{'{#REDISPORT}':r}]
print json.dumps({'data':ports},sort_keys=True,indent=4,separators=(',',':'))
