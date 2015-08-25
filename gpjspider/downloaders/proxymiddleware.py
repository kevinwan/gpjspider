# -*- coding: utf-8 -*-
import random
from datetime import date
from scrapy import log
# from gpjspider.spiders.base_spiders.gpjbasespider import GPJBaseSpider
from gpjspider.utils import get_redis_cluster
import base64
# import ipdb


class ProxyMiddleware(object):

    """
    被各网站被屏蔽时的判断
    """
    # judgement = {
    #     '58.com': ur'58.com/firewall',
    #     'ganji.com': ur'ganji.com/sorry/confirm.php',
    #     'baixing.com': ur'Service Unavailable',
    # }

    def __init__(self, settings):
        self.PROXIES = settings.getlist('PROXIES')
        self.good_proxy = random.choice(self.PROXIES)
        self.proxy_user_passwd = settings.getlist('PROXY_USER_PASSWD')[0]
        self.encoded_user_passwd = base64.encodestring(self.proxy_user_passwd)
        self.domains = settings.getlist('PROXY_DOMAINS')
        self.redis = get_redis_cluster()
        self.need_proxy = False

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def ip_control(self, response, spider):
        if response.headers.get('x-proxymesh-ip'):
            invalid_ip_key = spider.domain + str(date.today())
            self.redis.sadd(invalid_ip_key, response.headers['x-proxymesh-ip'])
            spider.log(u'OneForbiddenIP is {0}'.format(response.headers['x-proxymesh-ip']), log.INFO)

    def process_request(self, request, spider):
        if self.need_proxy:
            key_redis_domain = spider.domain + str(date.today())
            try:
                request.meta['proxy'] = self.good_proxy
                request.headers['Proxy-Authorization'] = 'Basic ' + self.encoded_user_passwd
                request.headers['x-proxymesh-not-ip'] = ",".join(self.redis.smembers(key_redis_domain))
            except Exception, e:
                spider.log(u'ExceptionInfo:{0}'.format(e))
            else:
                if not request.headers['x-proxymesh-not-ip']:
                    spider.log(u'ForbiddenIps are {0}'.format(request.headers['x-proxymesh-not-ip']), log.INFO)

    def process_response(self, request, response, spider):
        if response.status != 200:
            self.redis.sadd(spider.domain, response.url)
            self.ip_control(response, spider)
            self.need_proxy = True

        return response
