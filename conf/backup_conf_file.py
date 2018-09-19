#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
  例：将远程应用的配置文件拉到本地备份目录，下面将192.168.10.31上nginx的配置，拉到本地备份目录
      sudo python conf_dump.py  /usr/local/openresty/nginx/conf  192.168.10.31  nginx
"""

import sys        
import os        
import time        
import smtplib        
import pexpect
import shutil
from email.mime.text import MIMEText
from email.header import Header


conf_path  = sys.argv[1]
host_ip    = sys.argv[2]
item_name  = sys.argv[3]
fir_pa = str(conf_path)
sec_pa = str(host_ip)
thd_pa = str(item_name)
tmp_path = '/data/backup/config/tmp'
tmp_dir  = {fir_pa : tmp_path+'/'+thd_pa}
conf_dir = {fir_pa : fir_pa+'/'+'*'}
tmp_conf = tmp_dir.get(fir_pa)
item_conf = conf_dir.get(fir_pa)
date1 = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))


if os.path.exists(tmp_conf):
    pass
else:
    os.makedirs(tmp_conf)

def copyfile():
    child = pexpect.spawn("scp -r sss@%s:%s  %s" % (sec_pa, item_conf, tmp_conf))
    child.expect('password:')
    child.sendline('sss900318')
    child.expect('$')
    child.interact()

try:
    copyfile()
except :
    pass


backup_dir = '/data/backup/config/'
backup_file = backup_dir + host_ip + thd_pa + '_' + time.strftime('%Y%m%d%H%M%S' + '.tar.gz')
tar_command = "tar -czvf '%s' %s" % (backup_file, tmp_conf)
date2 = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))


if os.system(tar_command) == 0:
    print '\nResult:'
    print 'Successful backup to', backup_file
    size = os.path.getsize(backup_file)
    sender = 'clr@monitor.bcp'
    #receiver = ['sss@happy.cn', 'ddd@happy.cn']
    receiver = ['sss@happy.cn']
    message = MIMEText("%s 配置文件，\n%s 开始备份，\n%s 备份结束，\n文件名称：%s，\n文件大小：%.2fK" % (thd_pa, date1, date2, backup_file, (size/1024.0)) ,  'plain', 'utf-8')
    message['From'] = "clr@monitor.bcp"
    #message['To'] = "sss@happy.cn,ddd@happy.cn"
    message['To'] = "sss@happy.cn"
    subject = ("%s %s 备份完成" % (sec_pa, thd_pa))
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP('localhost')
        smtpObj.sendmail(sender, receiver, message.as_string())
        print "邮件发送成功"
    except smtplib.SMTPException:
        print "Error: 无法发送邮件"
        smtpObj.quit()
else:
    print '\nResult:'
    print 'Backup failed'
    sender = 'clr@monitor.bcp'
    #receiver = ['sss@happy.cn', 'ddd@happy.cn']
    receiver = ['sss@happy.cn']
    message = MIMEText("%s 配置文件, \n%s 开始备份，\n%s 备份结束" % (thd_pa, date1, date2), 'plain', 'utf-8')
    message['From'] = "clr@monitor.bcp"
    #message['To'] = "sss@happy.cn,ddd@happy.cn"
    message['To'] = "sss@happy.cn"
    subject = ("%s %s 备份失败" % (sec_pa, thd_pa))
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP('localhost')
        smtpObj.sendmail(sender, receiver, message.as_string())
        print "邮件发送成功"
    except smtplib.SMTPException:
        print "Error: 无法发送邮件"
        smtpObj.quit()

shutil.rmtree(tmp_conf)
