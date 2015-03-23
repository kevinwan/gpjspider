# -*- coding: utf-8 -*-
import urllib
from copy import deepcopy
import scrapy
from scrapy import log
from scrapy.http import Request
from gpjspider.items import BrandModelItem


class BrandModelBaixingSpider(scrapy.Spider):
    name = "brand_model_baixing"
    allowed_domains = ["baixing.com"]
    start_urls = (
        'http://china.baixing.com/ershouqiche/',
    )

    def parse(self, response):
        # rule = '//div[@class="fieldset "]/div[@class="items"][last()]/a'
        rule = u'//div[@class="fieldset "]/h4[contains(text(), "品牌")]/following-sibling::div/a'
        bs = response.xpath(rule)
        if not bs:
            self.log(u'品牌规则失效：{0}'.format(rule), level=log.ERROR)
            yield None

        for b in bs:
            try:
                brand = b.xpath('text()').extract()[0].strip()
                slug = b.xpath('@href').extract()[0].strip()
            except:
                self.log(u'小规则失效', level=log.ERROR)
                continue
            else:
                if u'不限' in brand or u'更多' in brand:
                    continue
                item = BrandModelItem()
                item['mum'] = None
                item['parent'] = brand
                item['domain'] = 'baixing.com'
                item['url'] = 'http://china.baixing.com' + slug
                item['slug'] = slug.strip('/').split('/')[-1]
                item['name'] = None
                request = Request(item['url'], callback=self.parse_model)
                request.meta['item'] = item
                yield request

    def parse_model(self, response):
        rule = '//div[@class="items all-items"]/a'
        rule = u'//h4[contains(text(), "车系列")]/following-sibling::div/a'
        ms = response.xpath(rule)
        if not ms:
            msg = u'型号规则失效：{0}：{1}'.format(rule, response.url)
            self.log(msg, level=log.ERROR)
            yield None
        for m in ms:
            try:
                model_name = m.xpath('text()').extract()[0].strip()
                slug = m.xpath('@href').extract()[0].strip()
                slug = str(slug)
                slug = urllib.url2pathname(slug).decode('utf-8')
            except:
                import traceback
                s = traceback.format_exc()
                self.log(u'小规则失效:{0}'.format(response.url + s), level=log.ERROR)
                continue
            else:
                if u'不限' in model_name or u'更多' in model_name or u'其他' in model_name:
                    continue
                item = deepcopy(response.meta['item'])
                item['name'] = model_name
                item['url'] = 'http://china.baixing.com' + slug
                item['slug'] = slug.strip('/').split('/')[-1]
                if '_' in item['slug']:
                    item['slug'] = item['slug'].split('_')[-1]
                yield item
        response.meta['item']['name'] = response.meta['item']['parent']
        response.meta['item']['parent'] = None
        yield response.meta['item']
