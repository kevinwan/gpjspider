# -*- coding: utf-8 -*-
from copy import deepcopy
import scrapy
from scrapy import log
from scrapy.http import Request
from gpjspider.items import BrandModelItem


class BrandModelXcarSpider(scrapy.Spider):
    name = "brand_model_xcar"
    allowed_domains = ["used.xcar.com.cn"]
    start_urls = (
        'http://used.xcar.com.cn/search',
    )

    def parse(self, response):
        rule = '//dd[@id="car_filter_pbid"]/div[@class="ulcon"]/a'
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
                item['domain'] = 'used.xcar.com.cn'
                item['parent'] = brand_name
                item['slug'] = url.strip('/').split('/')[-1]
                s = item['slug'].split('-')
                if not(len(s) == 17 and '0' < s[6] < '999999999'):
                    self.log(u'品牌slug小规则失效', level=log.ERROR)
                    yield
                item['slug'] = s[6]
                item['url'] = 'http://used.xcar.com.cn' + url
                item['name'] = None
                item['mum'] = None
                request = Request(item['url'], callback=self.parse_model)
                request.meta['item'] = item
                yield request

    def parse_model(self, response):
        """
        """
        rule = '//div[@id="pserids"]/p'
        ms = response.xpath(rule)
        if not ms:
            msg = u'型号规则失效:{0}:{1}'.format(rule, response.url)
            self.log(msg, level=log.ERROR)
            yield None
        for m in ms:
            mum = m.xpath('b/text()').extract()
            if not mum:
                continue
            else:
                mum = mum[0].strip(' ').strip(':')
            for model in m.xpath('span/a'):
                model_name = model.xpath('text()').extract()[0].strip()
                url = model.xpath('@href').extract()[0].strip()
                item = deepcopy(response.meta['item'])
                item['mum'] = mum
                item['name'] = model_name
                item['slug'] = url.strip('/').split('/')[-1]
                s = item['slug'].split('-')
                if not(len(s) == 17 and '0' < s[6] < '999999999'):
                    self.log(u'品牌slug小规则失效', level=log.ERROR)
                    yield
                item['slug'] = s[6]
                item['url'] = 'http://used.xcar.com.cn' + url
                yield item
        response.meta['item']['name'] = response.meta['item']['parent']
        response.meta['item']['parent'] = None
        yield response.meta['item']
