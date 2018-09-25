#!/usr/bin/python
#coding=utf-8

import os

f_curl = open('/data/scripts/url.txt')
line_curl = f_curl.readline()
url_curl = str(line_curl)
curl_w = "%{url_effective}'\n'"
http_code = "%{http_code}'\n'"

f_out1 = open('/data/scripts/out_curl.txt', 'w')
f_out1.write('')
f_out1.close()

for url_curl in f_curl:
    fscan1 = os.popen("curl -w 'clr_url--> '%s\'clr_http_code--> '%s  -I  %s" % (curl_w, http_code, url_curl))
    fcurl = fscan1.read()
    f_out1 = open('/data/scripts/out_curl.txt', 'a')
    f_out1.write(fcurl)
    f_out1.close()
f_curl.close()

os.system("sed -i -e '/clr/!d' /data/scripts/out_curl.txt")


f_nmap = open('/data/scripts/ip.txt')
line_nmap = f_nmap.readline()
ip_nmap = str(line_nmap)

f_out2 = open('/data/scripts/out_nmap.txt', 'w')
f_out2.write('')
f_out2.close()

for ip_nmap in f_nmap:
    fscan2 = os.popen('nmap -sT -sU -p1-100 -Pn -n -T5  %s' % ip_nmap)
    fnmap = fscan2.read()
    f_out2 = open('/data/scripts/out_nmap.txt', 'a')
    f_out2.write(fnmap)
    f_out2.close()
f_nmap.close()

os.system("sed -i -e '/open\|report/!d' /data/scripts/out_nmap.txt;sed -i '/filtered/'d /data/scripts/out_nmap.txt")
