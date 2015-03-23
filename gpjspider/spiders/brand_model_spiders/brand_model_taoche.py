# -*- coding: utf-8 -*-
import traceback
from copy import deepcopy
import scrapy
from scrapy import log
from scrapy.http import Request
from gpjspider.items import BrandModelItem


class BrandModelTaocheSpider(scrapy.Spider):
    name = "brand_model_taoche"
    allowed_domains = ["taoche.com"]
    start_urls = (
        'http://www.taoche.com/all/',
    )

    def parse(self, response):
        rule = '//div[@class="pinp_main"]/div/p/a'
        brands = response.xpath(rule)
        if not brands:
            self.log(u'品牌规则失效:{0}'.format(rule), level=log.ERROR)
            yield None
        for brand in brands:
            try:
                brand_name = brand.xpath('text()').extract()[0].strip()
                brand_slug = brand.xpath('@href').extract()[0].strip()
            except:
                exception_info = traceback.format_exc()
                msg = u'品牌规则失效2:\n{0}'.format(exception_info)
                self.log(msg, level=log.ERROR)
                continue
            else:
                if u'不限' in brand_name or u'全部' in brand_name:
                    continue
                item = BrandModelItem()
                item['domain'] = 'taoche.com'
                item['parent'] = brand_name.strip().split(' ')[-1]
                item['slug'] = brand_slug.strip('/').split('/')[-1]
                item['url'] = 'http://www.taoche.com' + brand_slug
                item['name'] = None
                item['mum'] = None
                request = Request(item['url'], callback=self.parse_model)
                request.meta['item'] = item
                yield request

    def parse_model(self, response):
        """
        """
        base_rule = '//dd[@id="logwtserial"]/ul/li/a'
        rule = '//li[@id="p_AllSerial"]/div/div/div/div/p/a'
        car_models = response.xpath(base_rule)
        car_models_2 = response.xpath(rule)
        car_models.extend(car_models_2)
        if not car_models:
            msg = u'型号规则失效:{0}:{1}'.format(rule, response.url)
            self.log(msg, level=log.ERROR)
            yield None
        for car_model in car_models:
            item = deepcopy(response.meta['item'])
            item['name'] = car_model.xpath('text()').extract()[0]
            if u'不限' in item['name'] or u'全部' in item['name'] or u'更多' in item['name']:
                continue
            slug = car_model.xpath('@href').extract()[0]
            item['slug'] = slug.strip().strip('/')
            item['url'] = 'http://www.taoche.com' + slug.strip()
            yield item
        response.meta['item']['name'] = response.meta['item']['parent']
        response.meta['item']['parent'] = None
        yield response.meta['item']
