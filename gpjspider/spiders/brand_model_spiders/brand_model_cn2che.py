# -*- coding: utf-8 -*-
from copy import deepcopy
import scrapy
from scrapy import log
from gpjspider.items import BrandModelItem


class BrandModelCn2cheSpider(scrapy.Spider):
    name = "brand_model_cn2che"
    allowed_domains = ["cn2che.com"]
    start_urls = (
        'http://www.cn2che.com/pinpai.html',
    )

    def parse(self, response):
        # rule = '//div[@class="brandlist"]//div[@class="msglist11"]/dl'
        rule = '//div[@class="brandlist"]//div[@class="msglist09"]'
        bs = response.xpath(rule)
        if not bs:
            self.log(u'品牌规则失效：{0}'.format(rule), level=log.ERROR)
            yield None

        for b in bs:
            try:
                brand = b.xpath('div[@class="msglist10"]/a/text()').extract()[0]
                slug = b.xpath('div[@class="msglist10"]/a/@href').extract()[0]
                car_mums = b.xpath('div[@class="msglist11"]/dl')
            except:
                self.log(u'aaaaaaaaa', level=log.ERROR)
            else:
                p_item = BrandModelItem()
                p_item['parent'] = brand.strip()
                p_item['domain'] = 'cn2che.com'
                p_item['url'] = 'http://www.cn2che.com' + slug.strip()
                p_item['slug'] = slug.strip().strip('/').split('/')[-1]
                p_item['name'] = None
                p_item['mum'] = None
                for a in car_mums:
                    mum = a.xpath('dt/a/text()').extract()[0]
                    for car_model in a.xpath('dd/a/span/..'):
                        item = deepcopy(p_item)
                        item['name'] = car_model.xpath('span/text()').extract()[0].strip()
                        slug = car_model.xpath('@href').extract()[0].strip()
                        item['slug'] = slug.strip().strip('/').split('/')[-1]
                        item['url'] = 'http://www.cn2che.com' + slug.strip()
                        item['mum'] = mum
                        yield item
                p_item['name'] = p_item['parent']
                p_item['parent'] = None
                yield p_item
