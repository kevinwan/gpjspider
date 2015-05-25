# -*- coding: utf-8 -*-
"""

"""
import random
import urlparse
import requests
from scrapy import log
from scrapy.http import HtmlResponse
from gpjspider.spiders.base_spiders.gpjbasespider import GPJBaseSpider
from gpjspider.utils import get_redis_cluster


class ProxyMiddleware(object):

    """
    代理
    """
    # 需要使用代理的 domain
    domains = (
        '58.com', #'ganji.com', 'souche.com', 
        # 'baixing.com', '273.cn', 'ganji.com',
        # 'autohome.com', 'pahaoche.com',
        # 'hx2car.com', 'zg2sc.cn', 'che168.com', 'souche.com'
    )

    def __init__(self, settings):
        self.redis = get_redis_cluster()
        self.good_proxies = settings.getlist('PROXIES')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_request(self, request, spider):
        # if spider.proxy_ips:
        for domain in self.domains:
            ip = None
            if domain in request.url:
                if isinstance(spider, GPJBaseSpider):
                    if not spider.proxy_ips:
                        spider.proxy_ips = spider.get_proxy_ips()
                    if spider.proxy_ips:
                        ip = random.choice(spider.proxy_ips)
                    else:
                        ip = self.redis.srandmember('valid_proxy_ips')
                else:
                    ip = self.redis.srandmember('valid_proxy_ips')
                if ip:
                    proxy = 'http://' + ip
                    request.meta['proxy'] = proxy
                    spider.log(
                        u'{0} with proxy {1}'.format(request.url, proxy), log.INFO)
                    # error_urls = (
                    #     '58.com', 'souche.com', 'ganji.com',
                    # )
                    # for error_url in error_urls:
                    #     if error_url in request.url:
                    try:
                        proxies = {
                            'http': random.choice(self.good_proxies)
                        }
                        response = requests.get(request.url, proxies=proxies)
                    except:
                        pass
                    else:
                        # spider.log(
                        #     u'Redirected to {0}'.format(response.url), log.INFO)
                        # u = urlparse.urlparse(response.url)
                        # url = u.scheme + '://' + u.netloc + u.path
                        url = response.url
                        return HtmlResponse(url, body=response.text, encoding='utf-8')
                else:
                    spider.log(u'{0} 找不到代理，放弃'.format(request.url), log.INFO)
            else:
                if 'proxy' in request.meta:
                    del request.meta['proxy']
