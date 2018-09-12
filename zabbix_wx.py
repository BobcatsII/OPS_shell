#!/usr/bin/env python
#coding: utf-8

"""
  zabbix 微信告警短信
  测试：python zabbix_wx.py user title text
"""

import json
import sys
import requests
import pdb 

#pdb.set_trace() 
class WeChatMSG(object):
    def __init__(self,content):
        self.gettoken_url = 'https://sssx.weixin.qq.com/cgi-bin/gettoken'
        self.gettoken_content = {
                            'corpid' : 'wx34e63d',
                            'corpsecret' : 'UF_dKkrhWfbkBE9AOsaIft4eZ' ,
                            }
        self.main_content = {
                            "touser":touser,
			                      #"toparty":"3",
                            "agentid":"1",
                            "msgtype": "text",
                            "text":{
                            "content":content,
                                    }
                            }
        self.sendmsg_url = 'https://sssx.weixin.qq.com/cgi-bin/message/send?access_token='


    def gettoken(self,url,data):
        result = requests.get(url, params=data, verify=False)
        token = json.loads(result.text)['access_token']
        return token

    def send_message(self,url,token,data):
        result = requests.post(url+token, data=json.dumps(data,ensure_ascii=False), verify=False)
        #result = requests.post(url+token, data=json.dumps(data))
        return result.text

if __name__ == '__main__':
    if len(sys.argv) == 4:
        touser,unusetitle,content = sys.argv[1:]
    else:
        print 'error segments, now exit'
        sys.exit()
    msg = WeChatMSG(content)
    access_token = msg.gettoken(msg.gettoken_url, msg.gettoken_content)
    print msg.send_message(msg.sendmsg_url,access_token,msg.main_content)



