# -*- coding: utf-8 -*-
import random
from datetime import date
from scrapy import log
# from gpjspider.spiders.base_spiders.gpjbasespider import GPJBaseSpider
from gpjspider.utils import get_redis_cluster
import base64
import socket
import ipdb


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
        self.need_proxy_domain = None
        self.server_id = '127.0.0.1'
        try:
            csock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            csock.connect(('8.8.8.8', 80))
            (addr, port) = csock.getsockname()
            csock.close()
            self.server_id = addr
        except Exception, e:
            log(u'ExceptionInfo:{0}'.format(e))

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def _need_proxy_domain(self, spider):
        if self.need_proxy_domain is None:
            self.need_proxy_domain = spider.domain in self.domains
        return self.need_proxy_domain

    def ip_control(self, response, spider):
        proxymesh_ip = response.headers.get('x-proxymesh-ip')
        if proxymesh_ip:
            invalid_ip_key = '%s_%s_%s' % (self.server_id, spider.domain, str(date.today()))
            self.redis.sadd(invalid_ip_key, proxymesh_ip)
            self.redis.expire(invalid_ip_key, 1200)
            spider.log(u'OneForbiddenIP is {0}'.format(
                proxymesh_ip), log.INFO)

    def process_request(self, request, spider):
        if self._need_proxy_domain(spider) and self.need_proxy:
            key_redis_domain = '%s_%s_%s' % (self.server_id, spider.domain, str(date.today()))
            try:
                request.meta['proxy'] = self.good_proxy
                request.headers[
                    'Proxy-Authorization'] = 'Basic ' + self.encoded_user_passwd
                request.headers[
                    'x-proxymesh-not-ip'] = ",".join(self.redis.smembers(key_redis_domain))
            except Exception, e:
                spider.log(u'ExceptionInfo:{0}'.format(e))
            else:
                forbidden_ips = request.headers.get('x-proxymesh-not-ip')
                if forbidden_ips:
                    spider.log(u'ForbiddenIps are {0}'.format(forbidden_ips, log.INFO))

    def process_response(self, request, response, spider):
        status = response.status
        if self._need_proxy_domain(spider) and status != 200:
            key = '%s_%s_%s' % (self.server_id, spider.domain, status)
            key_url = '%s_%s_%s' % (self.server_id, response.url, str(date.today()))
            self.redis.sadd(key, response.url)
            self.ip_control(response, spider)
            self.need_proxy = True
            request = spider.make_requests_from_url(response.url)
            self.redis.lpush(key_url, "Count")
            if 0 < self.redis.llen(key_url) < 3:
                return request
            else:
                self.redis.delete(key_url)
                return response
        else:
            return response
