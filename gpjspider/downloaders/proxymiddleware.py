# -*- coding: utf-8 -*-
"""

"""
import urlparse
import requests
import redis
from scrapy import log
from scrapy.http import HtmlResponse


redis_conn = redis.StrictRedis()


class ProxyMiddleware(object):
    """
    代理
    """
    # 需要使用代理的 domain
    domains = (
        '58.com',  'baixing.com', 'ganji.com', '273.cn', 'iautos.cn', 'che168.com',
        'youche.com', 'autohome.com', 'pahaoche.com', 'hx2car.com', 'zg2sc.cn',
        'souche.com'
    )

    def process_request(self, request, spider):
        for domain in self.domains:
            if domain in request.url:
                ip = redis_conn.srandmember('valid_proxy_ips')
                if ip:
                    proxy = 'http://' + ip
                    request.meta['proxy'] = proxy
                    spider.log(u'{0}应用了代理{1}'.format(request.url, proxy), log.INFO)
            else:
                if 'proxy' in request.meta:
                    del request.meta['proxy']

        error_urls = ('click.ganji.com', 'jing.58.com', 'jump.zhineng.58.com')
        for error_url in error_urls:
            if error_url in request.url:
                try:
                    ip = redis_conn.srandmember('valid_proxy_ips')
                    if ip:
                        response = requests.get(request.url, proxies={"http": 'http://' + ip})
                    else:
                        response = requests.get(request.url)
                except:
                    pass
                else:
                    spider.log(u'重定向到{0}'.format(response.url), log.INFO)
                    u = urlparse.urlparse(response.url)
                    url = u.scheme + '://' + u.netloc + u.path
                    request.meta['item']['url'] = url
                    return HtmlResponse(url, body=response.text, encoding='utf-8')
