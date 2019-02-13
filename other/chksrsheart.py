#!/usr/bin/python2.6
# -*- coding:utf-8 -*-

import os
import requests
import json
import time
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    filename='/data/log/srs/check_srs_heart.log',
                    datafmt="%Y/%m/%d %H:%M:%S",
                    format="%(asctime)s [%(levelname)s] %(message)s")

for i in xrange(144):
    try:
        logger.info("---------------------开始检查中心节点SRS接口服务---------------------")
        req = requests.get("http://127.0.0.1:11985/api/v1/streams")
        codenum = json.loads(req.text)['code']
        if codenum == 0:
            logger.info("检查srs-api心跳接口正常，code当前状态:{0}".format(codenum))
            logger.info("----------中心节点SRS接口服务正常----------")
            time.sleep(300)
            continue
        else:
            logger.info("+++++++++++++++++++++++中心节点SRS接口服务异常+++++++++++++++++++++++")
            logger.info(" 重启srs服务")
            srs_stat2 = os.system("/etc/init.d/srs restart")
            while 1:
                if srs_stat2 == 0:
                    logger.info("srs服务已重启完成")
                    break
                else:
                    logger.info("srs服务重启失败,再次重启")
                    srs_stat2 = os.system("/etc/init.d/srs restart")
                    continue
            logger.info("重启srs-api服务")
            srs_stat1 = os.system("/etc/init.d/srs-api restart")
            while 1:
                if srs_stat1 == 0:
                    logger.info("srs-api服务已重启完成")
                    break
                else:
                    logger.info("srs-api服务重启失败,再次重启")
                    srs_stat1 = os.system("/etc/init.d/srs-api restart")
                    continue

    except Exception, e:
        logger.info("+++++++++++++++++++++++中心节点SRS接口服务异常+++++++++++++++++++++++")
        logger.info("《《《《《《《重启srs服务》》》》》》》")
        srs_stat2 = os.system("/etc/init.d/srs restart")
        while 1:
            if srs_stat2 == 0:
                logger.info("srs服务已重启完成")
                break
            else:
                logger.info("srs服务重启失败,再次重启")
                srs_stat2 = os.system("/etc/init.d/srs restart")
                continue
        logger.info("《《《《《《《重启srs-api服务》》》》》》》")
        srs_stat = os.system("/etc/init.d/srs-api restart")
        while 1:
            if srs_stat == 0:
                logger.info("srs-api服务已重启完成")
                break
            else:
                logger.info("srs-api服务重启失败,再次重启")
                srs_stat = os.system("/etc/init.d/srs-api restart")
                continue
        time.sleep(300)
        continue
