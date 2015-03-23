# -*- coding: utf-8 -*-
from copy import deepcopy
import scrapy
from scrapy import log
from scrapy.http import Request
from gpjspider.items import BrandModelItem


class BrandModelIautosSpider(scrapy.Spider):
    name = "brand_model_iautos"
    allowed_domains = ["iautos.cn"]
    start_urls = (
        'http://so.iautos.cn/quanguo/',
    )

    def parse(self, response):
        rule = '//div[@id="xzpp_list"]/dl/dd/a'
        brands = response.xpath(rule)
        if not brands:
            self.log(u'品牌规则失效:{0}'.format(rule), level=log.ERROR)
            yield None
        for brand in brands:
            try:
                brand_name = brand.xpath('text()').extract()[0]
                brand_url = brand.xpath('@href').extract()[0]
            except:
                self.log(u'品牌小规则失效', level=log.DEBUG)
                continue
            else:
                item = BrandModelItem()
                item['parent'] = brand_name.strip()
                item['url'] = 'http://so.iautos.cn' + brand_url
                item['domain'] = 'iautos.cn'
                item['slug'] = brand_url.strip().strip('/').split('/')[-1]
                item['name'] = None
                item['mum'] = None
                request = Request(item['url'], callback=self.parse_model)
                request.meta['item'] = item
                yield request

    def parse_model(self, response):
        """
        """
        rule = u'//dt[contains(text(), "车系")]/following-sibling::dd/p/a'
        ms = response.xpath(rule)
        if not ms:
            self.log(u'型号规则失效:{0}:{1}'.format(rule, response.url), level=log.ERROR)
            yield None

        for m in ms:
            item = deepcopy(response.meta['item'])
            try:
                item['name'] = m.xpath('text()').extract()[0]
                item['url'] = 'http://so.iautos.cn' + m.xpath('@href').extract()[0].strip()
            except:
                continue
            item['slug'] = item['url'].strip('/').split('/')[-1]
            yield item
        response.meta['item']['name'] = response.meta['item']['parent']
        response.meta['item']['parent'] = None
        yield response.meta['item']
