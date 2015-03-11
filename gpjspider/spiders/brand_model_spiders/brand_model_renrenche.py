# -*- coding: utf-8 -*-
from copy import deepcopy
import scrapy
from scrapy import log
from scrapy.http import Request
from gpjspider.items import BrandModelItem


class BrandModelRenrencheSpider(scrapy.Spider):
    name = "brand_model_renrenche"
    allowed_domains = ["renrenche.com"]
    start_urls = (
        'http://www.renrenche.com/bj/ershouche',
    )

    def parse(self, response):
        rule = '//dl[@class="brand-more-area"]/dd/a'
        brands = response.xpath(rule)
        if not brands:
            self.log(u'品牌规则失效:{0}'.format(rule), level=log.ERROR)
            yield None
        for brand in brands:
            try:
                brand_name = brand.xpath('text()').extract()[0].strip()
                url = brand.xpath('@href').extract()[0].strip()
            except:
                self.log(u'品牌小规则失效', level=log.ERROR)
                continue
            else:
                item = BrandModelItem()
                item['domain'] = 'renrenche.com'
                item['parent'] = brand_name
                item['slug'] = url.strip('/').split('/')[-1]
                item['url'] = 'http://www.renrenche.com' + url
                item['name'] = None
                request = Request(item['url'], callback=self.parse_model)
                request.meta['item'] = item
                yield request

    def parse_model(self, response):
        """
        """
        rule = '//ul[@class="nav series"]/li/a[@id]'
        models = response.xpath(rule)
        if not models:
            msg = u'型号规则失效:{0}:{1}'.format(rule, response.url)
            self.log(msg, level=log.ERROR)
            yield None
        for model in models:
            model_name = model.xpath('text()').extract()[0].strip()
            url = model.xpath('@href').extract()[0].strip()
            item = deepcopy(response.meta['item'])
            item['name'] = model_name
            item['slug'] = url.strip('/').split('/')[-1]
            item['url'] = 'http://www.renrenche.com' + url
            yield item
        response.meta['item']['name'] = response.meta['item']['parent']
        response.meta['item']['parent'] = None
        yield response.meta['item']
