#!/usr/bin/python
"""
  短信告警
"""
import httplib, urllib
import sys
import commands 

username='User'
password='Passwd'
mobile=sys.argv[1]
content=sys.argv[2]
productid='887361'
dstime=''

params = urllib.urlencode({'username': username, 'password': password, 'mobile': mobile, \
		                           'content': content, 'productid': productid, 'dstime': dstime})
headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
conn = httplib.HTTPConnection("www.ztsms.cn:8800")
conn.request("POST", "/sendXSms.do", params, headers)
response = conn.getresponse()
data = response.read()
conn.close()
