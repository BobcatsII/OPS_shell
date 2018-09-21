#!/bin/bash
#source /etc/profile

port=$1
item=$3

case $2 in
    mntr)
        str=`echo mntr|nc 127.0.0.1 $port |grep $item|awk '{$1="";sub(" ", "");print}'`
    if [ -z "$str" ];then
        str=0
    fi
    echo $str
        ;;
    ruok)
        echo ruok|nc 127.0.0.1 $port
        ;;
esac
