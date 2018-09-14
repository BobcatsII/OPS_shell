#!/usr/bin/python
#coding:utf8
import redis
import sys

"""
  查询、删除redis的key
"""

class Redis_Config(object):
    def __init__(self,*args):
        self.login_host = login_host
        self.login_port = login_port
        self.login_db = login_db
        self.login_pwd = login_pwd

    def connection(self, login_host, login_port, login_db, login_pwd):
        self.client = redis.StrictRedis(host=login_host,port=login_port,db=login_db,password=login_pwd)

    def checkkey(self,ckey):
        self.chk_key = self.client.keys(ckey)
        if self.chk_key != []:
            self.keys = []
            for i in self.chk_key:
                self.keys.append(i)
                if i in self.chk_key:
                    self.keys.append('\n')
            for keys in self.keys:
               print keys,
        else:
            print ckey + " 不存在"

    def deletekey(self,dkey):
        self.del_key = self.client.delete(dkey)
        if self.del_key == 1:
            print dkey + " 已被删除"

login_pwd, login_host, login_port, login_db = [sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]]
c = Redis_Config()

if sys.argv[1] == 'checkkey':
    """
       checkkey passwds 172.17.0.165 7379 0 key
    """
    ckey = sys.argv[6]
    c.connection(login_host, login_port, login_db, login_pwd)
    c.checkkey(ckey)

if sys.argv[1] == 'deletekey':
    """
       deletekey passwds 172.17.0.165 7379 0 key
    """
    dkey = sys.argv[6]
    c.connection(login_host, login_port, login_db, login_pwd)
    c.deletekey(dkey)
                               

#脚本执行完成会自动断开连接。      
