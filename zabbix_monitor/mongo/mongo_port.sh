#!/bin/bash

host=$1

if [ -z "$host" ];then
    port=`netstat -tlnp |grep mongo |awk '{print $4}' |awk -F: '{print $2}'`
    if [ "$port" != "" ];then
        echo $port
    else
        echo 0
    fi
else
    echo "rs.printSlaveReplicationInfo();" |/usr/local/mongodb/bin/mongo --quiet $host:27017/admin -uroot -pdYKAMc9K |grep -A 2 $host |awk '{if(NR == 3) print $1}'
fi
