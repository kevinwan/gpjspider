# -*- coding: utf-8 -*-
"""

"""
import random
import urlparse
import requests
from rediscluster import RedisCluster
from scrapy import log
from scrapy.http import HtmlResponse
from gpjspider.spiders.base_spiders.gpjbasespider import GPJBaseSpider


class ProxyMiddleware(object):
    """
    代理
    """
    # 需要使用代理的 domain
    domains = (
        '58.com',  'baixing.com', 'ganji.com', '273.cn',
        'che168.com', 'autohome.com', 'pahaoche.com',
        'hx2car.com', 'zg2sc.cn', 'souche.com'
    )

    def __init__(self, settings):
        self.REDIS_CONFIG = settings.getlist('REDIS_CONFIG')
        self.good_proxies = settings.getlist('PROXIES')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_request(self, request, spider):
        for domain in self.domains:
            ip = None
            if domain in request.url:
                if isinstance(spider, GPJBaseSpider):
                    if not spider.proxy_ips:
                        spider.proxy_ips = spider.get_proxy_ips()
                    if spider.proxy_ips:
                        ip = random.choice(spider.proxy_ips)
                    else:
                        redis = RedisCluster(startup_nodes=self.REDIS_CONFIG)
                        ip = redis.srandmember('valid_proxy_ips')
                else:
                    redis = redis.StrictRedis()
                    ip = redis.srandmember('valid_proxy_ips')
                if ip:
                    proxy = 'http://' + ip
                    request.meta['proxy'] = proxy
                    spider.log(
                        u'{0}应用了代理{1}'.format(request.url, proxy), log.INFO)
                else:
                    spider.log(u'{0}找不到代理，放弃'.format(request.url), log.INFO)
                    return None
            else:
                if 'proxy' in request.meta:
                    del request.meta['proxy']

            error_urls = (
                'souche.com', 'ganji.com', 'click.ganji.com', 'jing.58.com',
                'jump.zhineng.58.com'
            )
            for error_url in error_urls:
                if error_url in request.url:
                    try:
                        proxies = {
                            'http': random.choice(self.good_proxies)
                        }
                        response = requests.get(request.url, proxies=proxies)
                    except:
                        pass
                    else:
                        spider.log(u'重定向到{0}'.format(response.url), log.INFO)
                        u = urlparse.urlparse(response.url)
                        url = u.scheme + '://' + u.netloc + u.path
                        return HtmlResponse(
                            url, body=response.text, encoding='utf-8')
