# -*- coding: utf-8 -*-
import random
from datetime import date
from scrapy import log
# from gpjspider.spiders.base_spiders.gpjbasespider import GPJBaseSpider
from gpjspider.utils import get_redis_cluster
import re
import base64
import ipdb


class ProxyMiddleware(object):

    """
    被各网站被屏蔽时的判断
    """
    juage = {
        '58.com': r'58.com/firewall',
        'ganji.com': r'ganji.com/sorry/confirm.php',
        'baixing.com': r'Service Unavailable',
    }

    def __init__(self, settings):
        # self.redis = get_redis_cluster()
        # self.good_proxies = settings.getlist('PROXIES')
        self.PROXIES = settings.getlist('PROXIES')
        self.good_proxy = random.choice(self.PROXIES)
        self.proxy_user_passwd = settings.getlist('PROXY_USER_PASSWD')[0]
        self.encoded_user_passwd = base64.encodestring(self.proxy_user_passwd)
        self.domains = settings.getlist('PROXY_DOMAINS')
        self.need_proxy = None
        self.r = get_redis_cluster()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def _need_proxy(self, request, spider):
        if self.need_proxy is None:
            self.need_proxy = spider.domain in self.domains
        return self.need_proxy

    def ip_control(self, response, spider):
        is_proxy = response.headers.has_key('x-proxymesh-ip')
        if (re.search(self.juage[spider.domain], response.headers.get('location', 'None')) or
                re.search(self.juage[spider.domain], response.body)) and is_proxy:
            invalid_ip_key = str(date.today())
            self.r.sadd(invalid_ip_key, response.headers['x-proxymesh-ip'])
            spider.log(
                u'OneForbiddenIP is {0}'.format(response.headers['x-proxymesh-ip']), log.INFO)
        else:
            pass

    def process_request(self, request, spider):
        if self._need_proxy(request, spider):
            today = str(date.today())
            try:
                request.meta['proxy'] = self.good_proxy
                request.headers['Proxy-Authorization'] = 'Basic ' + \
                    self.encoded_user_passwd
                request.headers[
                    'x-proxymesh-not-ip'] = ",".join(self.r.smembers(today))
            except:
                pass
            else:
                spider.log(
                    u'ForbiddenIps is {0}'.format(request.headers['x-proxymesh-not-ip']), log.INFO)
        else:
            return

    def process_response(self, request, response, spider):
        self.ip_control(response, spider)
        return response
