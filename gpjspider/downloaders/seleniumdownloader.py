# -*- coding: utf-8 -*-
"""
"""
from selenium import webdriver
from scrapy import log
from scrapy.http import HtmlResponse
from scrapy.exceptions import NotConfigured


class SeleniumDownloader(object):
    """
    页面需要执行 js 的
    """
    def __init__(self, selenium_domains=None):
        if not selenium_domains:
            self.selenium_domains = []
        else:
            self.selenium_domains = selenium_domains

    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.getlist('SELENIUM_DOMAINS'):
            raise NotConfigured
        return cls(crawler.settings.getlist('SELENIUM_DOMAINS'))

    def process_request(self, request, spider):
        for domain in self.selenium_domains:
            if domain.lower() in request.url:
                spider.log(u'用selenium请求{0}'.format(request.url), log.INFO)
                driver = webdriver.PhantomJS(port=5503)
                driver.get(request.url)
                elem = driver.find_element_by_xpath("//*")
                body = elem.get_attribute("outerHTML")
                driver.quit()
                return HtmlResponse(request.url, body=body, encoding='utf-8')
