# -*- coding: utf-8 -*-
from copy import deepcopy
import scrapy
from scrapy import log
from scrapy.http import Request
from gpjspider.items import BrandModelItem


class BrandModelSoucheSpider(scrapy.Spider):
    name = "brand_model_souche"
    allowed_domains = ["souche.com"]
    start_urls = (
        'http://www.souche.com/beijing/list',
    )

    def parse(self, response):
        rule = '//div[@class="list_allBrand_wrap"]/div/dl/dd/a'
        brands = response.xpath(rule)
        if not brands:
            self.log(u'品牌规则失效:{0}'.format(rule), level=log.ERROR)
            yield None
        for brand in brands:
            try:
                brand_name = brand.xpath('text()').extract()[0].strip()
                slug = brand.xpath('@href').extract()[0].strip()
            except:
                self.log(u'品牌小规则失效', level=log.ERROR)
                continue
            else:
                item = BrandModelItem()
                item['domain'] = 'souche.com'
                item['parent'] = brand_name
                item['slug'] = slug.strip('/').split('/')[-2]
                m = u'http://www.souche.com/beijing/{0}/list-mx2015'
                item['url'] = m.format(item['slug'])
                item['name'] = None
                item['mum'] = None
                request = Request(item['url'], callback=self.parse_model)
                request.meta['item'] = item
                yield request

    def parse_model(self, response):
        """
        """
        rule = '//div[@id="brand_option"]/div/ul'
        ms = response.xpath(rule)
        if not ms:
            msg = u'型号规则失效:{0}:{1}'.format(rule, response.url)
            self.log(msg, level=log.ERROR)
            yield None
        for m in ms:
            mum = m.xpath('div/text()').extract()[0]
            for model in m.xpath('/li/a'):
                model_name = model.xpath('text()').extract()[0].strip()
                url = model.xpath('@href').extract()[0].strip()
                item = deepcopy(response.meta['item'])
                item['mum'] = mum
                item['name'] = model_name
                item['slug'] = url.strip('/').split('/')[-2]
                item['url'] = 'http://www.souche.com' + url
                yield item
        response.meta['item']['name'] = response.meta['item']['parent']
        response.meta['item']['parent'] = None
        yield response.meta['item']
