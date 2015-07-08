# -*- coding: utf-8 -*-
import random
import urlparse
import requests
from scrapy import log
from scrapy.http import HtmlResponse
from gpjspider.spiders.base_spiders.gpjbasespider import GPJBaseSpider
from gpjspider.utils import get_redis_cluster


class ProxyMiddleware(object):
    domains = (
        '58.com', 'ganji.com', 'taoche.com',
        # 'baixing.com', '273.cn', 'ganji.com',
        # 'autohome.com', 'pahaoche.com',
        # 'hx2car.com', 'zg2sc.cn', 'che168.com', 'souche.com'
    )

    def __init__(self, settings):
        self.redis = get_redis_cluster()
        self.good_proxies = settings.getlist('PROXIES')
        self.domains = settings.getlist('PROXY_DOMAINS', self.domains)
        self.need_proxy = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def _need_proxy(self, spider):
        if self.need_proxy is None:
            self.need_proxy = spider.domain in self.domains
        return self.need_proxy

    def process_request(self, request, spider):
        if self._need_proxy(spider) and not request.dont_filter:
            ip = None
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
            # else:
            #     if 'proxy' in request.meta:
            #         del request.meta['proxy']
