# -*- coding: utf-8 -*-
"""
实用任务
"""
import time
import requests
from celery.utils.log import get_task_logger
from gpjspider import celery_app as app
from gpjspider import GPJSpiderTask
from rediscluster import RedisCluster


@app.task(name="check_proxy_ip", bind=GPJSpiderTask)
def check_proxy_ip(self):
    """
    """
    logger = get_task_logger('check_proxy_ip')
    logger.debug(u'开始检查可用代理IP,超过5秒为不可用代理')
    valid_key = 'valid_proxy_ips'
    invalid_key = 'invalid_proxy_ips'
    redis_conn = RedisCluster(startup_nodes=self.app.conf.REDIS_CLUSTERS)
    ips = redis_conn.smembers(valid_key)
    ips2 = redis_conn.smembers(invalid_key)
    ips.update(ips2)
    valid_ip_num = 0
    for ip in ips:
        try:
            start_time = time.time()
            requests.get('http://www.baidu.com',
                         proxies={"http": "http://"+ip},
                         timeout=(5, 2))
            end_time = time.time()
        except:
            pass
        else:
            t = end_time - start_time
            if t > 5:
                redis_conn.srem(valid_key, ip)
                redis_conn.sadd(invalid_key, ip)
                logger.debug(u"无效 IP:{0}".format(ip))
            else:
                redis_conn.sadd(valid_key, ip)
                redis_conn.srem(invalid_key, ip)
                logger.debug(u"有效 IP:{0}, {1}".format(ip, t))
                valid_ip_num += 1
    logger.info(u"一共有{0}个有效代理IP".format(valid_ip_num))
