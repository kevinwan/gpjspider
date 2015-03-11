# -*- coding: utf-8 -*-
import json
from copy import deepcopy
import scrapy
from scrapy import log
from scrapy.http import Request
from gpjspider.items import BrandModelItem


class BrandModelChe168Spider(scrapy.Spider):
    name = "brand_model_che168"
    allowed_domains = ["che168.com"]
    start_urls = (
        'http://www.che168.com/handler/usedcarlistv4.ashx?&action=brandlist&area=china',
    )

    def parse(self, response):
        json_str = response.body_as_unicode()
        try:
            js = json.loads(json_str)
        except:
            pass
        else:
            for j in js:
                item = BrandModelItem()
                item['domain'] = "che168.com"
                item['parent'] = j['name']
                item['slug'] = j['url'].strip().strip('/').split('/')[-1]
                item['url'] = 'http://www.che168.com' + j['url']
                item['name'] = None
                request = Request(item['url'], callback=self.parse_model)
                request.meta['item'] = item
                yield request

    def parse_model(self, response):
        """
        """
        rule = u'//ul[@id="SelectedConditions"]/li/div[contains(text(), "系")]/following-sibling::div/a[@title]'
        ms = response.xpath(rule)
        if not ms:
            self.log(u'型号规则失效', level=log.ERROR)
            yield None
        for m in ms:
            item = deepcopy(response.meta['item'])
            item['name'] = m.xpath('text()').extract()[0]
            item['url'] = m.xpath('@href').extract()[0]
            item['slug'] = item['url'].split('#')[0].strip('/').split('/')[-1]
            item['url'] = 'http://www.che168.com' + item['url'].split('#')[0]
            yield item
        response.meta['item']['name'] = response.meta['item']['parent']
        response.meta['item']['parent'] = None
        yield response.meta['item']






