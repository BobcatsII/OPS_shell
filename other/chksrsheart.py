#!/usr/bin/python2.6
#-*- coding:utf-8 -*-

import os
import requests
import json
import time
import logging

req = requests.get("http://127.0.0.1:11985/api/v1/streams")
codenum = json.loads(req.text)['code']
logging.basicConfig(level=logging.INFO,
                    filename='/data/log/srs/check_srs_heart.log',
                    datafmt="%Y/%m/%d %H:%M:%S",
                    format="%(asctime)s [%(levelname)s] %(message)s")

logger = logging.getLogger(__name__)

for i in xrange(3):
    if codenum == 0:
        logger.info("检查srs-api心跳接口正常，code当前状态:{0}".format(codenum))
        time.sleep(300)
        continue
    else:
        logger.info("当前srs-api心跳接口code不为0, 重启srs-api服务")
        srs_stat = os.system("/etc/init.d/srs-api restart")
        while 1:
            if srs_stat == 0:
                logger.info("srs-api服务已重启完成")
                break
            else:
                logger.warning("srs-api服务重启失败,再次重启")
                srs_stat = os.system("/etc/init.d/srs-api restart")
                continue
