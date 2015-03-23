# -*- coding: utf-8 -*-
import json
from copy import deepcopy
import scrapy
from scrapy import log
from scrapy.http import Request
from gpjspider.items import BrandModelItem


class BrandModel58comSpider(scrapy.Spider):
    name = "brand_model_58com"
    allowed_domains = ["58.com"]
    start_urls = (
        'http://quanguo.58.com/ershouche/',
    )

    def parse(self, response):
        base_rule = '//input[@id="data1"]/@value'
        try:
            s = response.xpath(base_rule).extract()[0]
        except:
            self.log(u'提取品牌 json 时失败。', level=log.ERROR)
        else:
            s = s.replace("'", '"')
            try:
                js = json.loads(s)
            except:
                self.log(u'转换成 json 时失败。', level=log.ERROR)
            else:
                for j in js:
                    item = BrandModelItem()
                    item['mum'] = None
                    item['parent'] = j['text'].strip()
                    if u'不限' in item['parent']:
                        continue
                    if (u'装载机' in item['parent'] or u'其他客车' in item['parent']
                    or u'推土机' in item['parent']):
                        continue

                    item['url'] = j['url'].strip()
                    item['domain'] = '58.com'
                    item['slug'] = item['url'].strip().strip('/').split('/')[-1]
                    request = Request(item['url'], self.parse_model)
                    request.meta['item'] = item
                    yield request

    def parse_model(self, response):
        """
        """
        base_rule = u'//dt[@class="secitem_brand" and contains(text(), "车系")]/following-sibling::dd/a'
        model_nodes = response.xpath(base_rule)
        if not model_nodes:
            self.log(u'规则失效:{0}:{1}'.format(base_rule, response.url))
            yield None

        for model_node in model_nodes:
            try:
                model_name = model_node.xpath('text()').extract()[0]
                url = model_node.xpath('@href').extract()[0]
            except:
                continue
            if model_name == u'不限':
                continue
            item = deepcopy(response.meta['item'])
            item['name'] = model_name
            item['url'] = url
            item['slug'] = url.strip().strip('/').split('/')[-1]
            yield item

        item = response.meta['item']
        item['name'] = item['parent']
        item['parent'] = None
        yield item
