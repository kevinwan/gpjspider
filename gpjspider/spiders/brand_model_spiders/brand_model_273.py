# -*- coding: utf-8 -*-
from copy import copy
import scrapy
from scrapy import log
from scrapy.http import Request
from gpjspider.items import BrandModelItem


class BrandModel273Spider(scrapy.Spider):
    name = "brand_model_273"
    allowed_domains = ["273.cn"]
    start_urls = (
        'http://www.273.cn/car/',
    )

    def parse(self, response):
        base_1_rule = '//ul[@class="js_more_list brand_list"]'
        base_2_rule = 'li/a'
        brand_rule = 'text()'
        url_rule = '@href'

        bs = response.xpath(base_1_rule)
        if not bs:
            self.log(u'获取品牌的1规则失效:{0}'.format(base_1_rule), level=log.ERROR)
            yield None

        for b in bs:
            brands = b.xpath(base_2_rule)
            if not brands:
                self.log(u'获取品牌的2规则失效:{0}'.format(base_2_rule), level=log.ERROR)
                yield None
            for brand in brands:
                item = BrandModelItem()
                item['mum'] = None
                item['domain'] = "273.cn"
                item['parent'] = brand.xpath(brand_rule).extract()[0].strip()
                if u'品牌' in item['parent']:
                    continue
                item['url'] = brand.xpath(url_rule).extract()[0].strip()
                if not item['parent'] or not item['url']:
                    self.log(u'无法获取品牌或者 url', level=log.ERROR)
                    yield None
                if 'http://www.273.cn' not in item['url']:
                    item['url'] = 'http://www.273.cn' + item['url']
                request = Request(item['url'], callback=self.parse_model)
                request.meta['item'] = item
                yield request

    def parse_model(self, response):
        """
        """
        base_rule = '//ul[@class="js_more_list"]/li/a'
        ms = response.xpath(base_rule)
        if not ms:
            msg = u'获取型号的规则失效:{0}:{1}'.format(base_rule, response.url)
            self.log(msg, level=log.ERROR)
            yield None

        for m in ms:
            model_name = m.xpath('text()').extract()
            model_url = m.xpath('@href').extract()
            if not model_name or not model_url:
                self.log(u'无法获取车系：{0}'.format(response.url), level=log.ERROR)
                yield None
            model_name = model_name[0].strip()
            if u'不限' in model_name:
                continue
            model_url = model_url[0].strip()
            item = copy(response.meta['item'])
            item['name'] = model_name
            if 'http://www.273.cn' not in model_url:
                item['slug'] = model_url.strip().strip('/').strip()
                item['url'] = 'http://www.273.cn' + model_url
                yield item
            else:
                self.log(u'获取 slug 错误：{0}'.format(model_url), level=log.ERROR)
                yield None
        # 保存品牌
        item['name'] = item['parent']
        item['parent'] = None
        item['slug'] = item['url'].strip().strip('/').split('/')[-1]
        yield item
