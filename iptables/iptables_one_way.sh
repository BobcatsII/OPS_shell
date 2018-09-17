#!/bin/bash

#需求：实现 192.168.10.*  网段不能访问 100/200 网段内的所有服务器 ，而 192.168.100/200.* 网段内的服务器可以访问 192.168.10.31 服务器

num=`/sbin/ifconfig -a|grep inet|grep -v 127.0.0.1|grep -v inet6|awk '{print $2}'|tr -d "addr:"|awk -F'.' '{print $3}'`

if [ $num == '100'] || [ $num == '200' ]
then
    iptables -A INPUT  -s 192.168.10.31 -m state --state RELATED,ESTABLISHED -j ACCEPT
    iptables -A INPUT  -s 192.168.10.0/255.255.255.0 -j DROP
else
    echo "The host is no longer in section 100/200"
fi
