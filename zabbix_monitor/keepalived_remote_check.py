#!/usr/bin/python
import sys
import os
import commands

INTERFACE="em1"
VIP=sys.argv[1]
ROLE=sys.argv[2]
try:
	LB_IP=sys.argv[3]
except:
	pass


if ROLE=="ping":
	command="/bin/ping %s -c 4 -W 4"%(VIP)
	ping_stat=commands.getstatusoutput(command)[0]
	print ping_stat
	sys.exit()

if ROLE=="master":
	command1="/you/path/zabbix/bin/zabbix_get -s %s -k system.hw.macaddr[%s,short]"%(VIP,INTERFACE)
	VIP_MAC=commands.getoutput(command1)
	command2="/you/path/zabbix/bin/zabbix_get -s %s -k system.hw.macaddr[%s,short]"%(LB_IP,INTERFACE)
	LB_MAC=commands.getoutput(command2)
	if VIP_MAC==LB_MAC:
		print 0
	else:
		print 1
	
elif ROLE=="backup":
	command1="/you/path/zabbix/bin/zabbix_get -s %s -k system.hw.macaddr[%s,short]"%(VIP,INTERFACE)
	VIP_MAC=commands.getoutput(command1)
	command2="/you/path/zabbix/bin/zabbix_get -s %s -k system.hw.macaddr[%s,short]"%(LB_IP,INTERFACE)
	LB_MAC=commands.getoutput(command2)
	if VIP_MAC==LB_MAC:
		print 1
	else:
		print 0

else:
	pass
