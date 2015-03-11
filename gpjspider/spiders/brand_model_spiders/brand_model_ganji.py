# -*- coding: utf-8 -*-
import json
from copy import deepcopy
import scrapy
from scrapy import log
from scrapy.http import Request
from gpjspider.items import BrandModelItem


class BrandModelGanjiSpider(scrapy.Spider):
    name = "brand_model_ganji"
    allowed_domains = ["ganji.com"]
    start_urls = (
        'http://bj.ganji.com/ajax.php?dir=vehicle&module=getNewLetterMajor'
        'Category&url=/ershouche/',
    )

    def parse(self, response):
        json_str = response.body_as_unicode()
        try:
            js = json.loads(json_str)
        except:
            self.log(u'', level=log.ERROR)
        else:
            brand_dicts = js.values()
            for brand_dict in brand_dicts:
                for slug, d in brand_dict.iteritems():
                    item = BrandModelItem()
                    item['parent'] = d['title']
                    item['slug'] = slug
                    item['url'] = "http://www.ganji.com/" + slug + '/'
                    item['domain'] = 'ganji.com'
                    item['name'] = None
                    request = Request(item['url'], callback=self.parse_model)
                    request.meta['item'] = item
                    yield request

    def parse_model(self, response):
        """
        """
        rule = '//dd[@class="posrelative"]/a[@class="a-circle"]'
        ms = response.xpath(rule)
        if not ms:
            self.log(u'型号规则失效:{0}:{1}'.format(rule, response.url), level=log.ERROR)
            yield None
        for m in ms:
            item = deepcopy(response.meta['item'])
            try:
                model_name = m.xpath('text()').extract()[0].strip()
                url = m.xpath('@href').extract()[0].strip()
            except:
                continue
            if u'不限' in model_name or u'更多' in model_name:
                continue
            item['name'] = model_name
            item['url'] = "http://www.ganji.com" + url
            item['slug'] = url.strip('/')
            yield item
        response.meta['item']['name'] = response.meta['item']['parent']
        response.meta['item']['parent'] = None
        yield response.meta['item']



