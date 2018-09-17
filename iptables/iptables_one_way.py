#!/usr/bin/python
#coding=utf-8

import iptc
import commands

"""
    需求：实现 192.168.10.*  网段不能访问 100/200 网段内的所有服务器 ，而 192.168.100/200.* 网段内的服务器可以访问 192.168.10.31 服务器
"""

num = commands.getoutput("/sbin/ifconfig -a|grep inet|grep -v 127.0.0.1|grep -v inet6|awk '{print $2}'|tr -d 'addr:'|awk -F'.' '{print $3}'")

if num == '100' or num == '200':
    rule = iptc.Rule()
    rule.src = "192.168.100.31"
    match = iptc.Match(rule, "state")
    match.state = "RELATED,ESTABLISHED"
    rule.add_match(match)
    rule.target = iptc.Target(rule, "ACCEPT")
    chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), "INPUT")
    chain.append_rule(rule)

    rule2 = iptc.Rule()
    rule2.src = '192.168.10.0/255.255.255.0'
    rule2.target = iptc.Target(rule2, "DROP")
    chain2 = iptc.Chain(iptc.Table(iptc.Table.FILTER), "INPUT")
    chain2.append_rule(rule2)
else:
    print "The host is no longer in section 100/200"
