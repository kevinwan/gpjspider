# -*- coding: utf-8 -*-
from copy import copy
import scrapy
from scrapy import log
from scrapy.http import Request
from gpjspider.items import BrandModelItem


class BrandModel51autoSpider(scrapy.Spider):
    name = "brand_model_51auto"
    allowed_domains = ["51auto.com"]
    start_urls = (
        'http://www.51auto.com/quanguo/search',
    )

    def parse(self, response):
        base_1_rule = '//ul[@id="info_dialog_brand"]/li/p/span/a'
        bs = response.xpath(base_1_rule)
        if not bs:
            self.log(u'找不到，基本规则：{0}'.format(base_1_rule), level=log.ERROR)
            yield None

        for b in bs:
            brand = b.xpath('text()').extract()
            url = b.xpath('@href').extract()
            if not brand or not url:
                continue
            brand = brand[0]
            url = url[0]
            item = BrandModelItem()
            item['domain'] = "51auto.com"
            item['parent'] = brand.strip()
            item['url'] = url.strip()
            request = Request(item['url'], callback=self.parse_model)
            request.meta['item'] = item
            yield request

    def parse_model(self, response):
        """
        """
        base_1_rule = '//a[@class="a_gray6"]'
        ms = response.xpath(base_1_rule)
        if not ms:
            self.log(u'找不到，基本车系规则：{0}'.format(base_1_rule), level=log.ERROR)
            yield None
        for m in ms:
            try:
                name = m.xpath('text()').extract()[0].strip()
                url = m.xpath('@href').extract()[0].strip()
            except:
                self.log(u'规则放生变化：{0}'.format(response.url), level=log.ERROR)
            else:
                item = copy(response.meta['item'])
                item['url'] = url
                item['name'] = name
                item['slug'] = url.strip().strip('/').split('/')[-1]
                yield item
