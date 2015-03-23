# -*- coding: utf-8 -*-
from copy import deepcopy
import scrapy
from scrapy import log
from scrapy.http import Request
from gpjspider.items import BrandModelItem


class BrandModelCheshiSpider(scrapy.Spider):
    name = "brand_model_cheshi"
    allowed_domains = ["cheshi.com"]
    start_urls = (
        'http://2sc.cheshi.com/china/',
    )

    def parse(self, response):
        rule = '//div[@id="showdiv"]/ul/li/span/a'
        bs = response.xpath(rule)
        if not bs:
            self.log(u'品牌规则失效:{0}'.format(rule), level=log.ERROR)
            yield None
        for b in bs:
            try:
                brand = b.xpath('text()').extract()[0]
                url = b.xpath('@href').extract()[0]
            except:
                self.log(u'', level=log.ERROR)
            else:
                item = BrandModelItem()
                item['mum'] = None
                item['parent'] = brand.strip()
                item['url'] = url.strip()
                item['slug'] = url.strip().strip('/').split('/')[-1]
                item['domain'] = 'cheshi.com'
                item['name'] = None
                request = Request(item['url'], callback=self.parse_model)
                request.meta['item'] = item
                yield request

    def parse_model(self, response):
        """
        """
        rule = u'//dt[contains(text(), "车系")]/following-sibling::dd/p/i'
        ms = response.xpath(rule)
        if not ms:
            msg = u'型号规则失效:{0}：{1}'.format(rule, response.url)
            self.log(msg, level=log.ERROR)
            yield None
        for m in ms:
            mum = m.xpath('text()').extract()[0]
            mum = mum.strip(u'：').strip()
            for m2 in m.xpath('following-sibling::a'):
                try:
                    model_name = m2.xpath('text()').extract()[0]
                    url = m2.xpath('@href').extract()[0]
                except:
                    self.log(u'', level=log.ERROR)
                else:
                    item = deepcopy(response.meta['item'])
                    item['name'] = model_name.strip()
                    item['url'] = url.strip()
                    item['mum'] = mum
                    item['slug'] = url.strip().strip('/').split('/')[-1]
                    yield item
        response.meta['item']['name'] = response.meta['item']['parent']
        response.meta['item']['parent'] = None
        yield response.meta['item']
