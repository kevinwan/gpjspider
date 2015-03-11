# -*- coding: utf-8 -*-
import scrapy
from scrapy import log
from gpjspider.items import BrandModelItem


class BrandModelHx2carSpider(scrapy.Spider):
    name = "brand_model_hx2car"
    allowed_domains = ["hx2car.com"]
    start_urls = (
        'http://www.hx2car.com/',
    )

    def parse(self, response):
        rule = '//div[@id="list"]/ul/li'
        bs = response.xpath(rule)
        if not bs:
            self.log(u'品牌规则失效：{0}'.format(rule), level=log.ERROR)
            yield None
        a = bs[::2]
        bs = bs[1::2]
        for idx, b in enumerate(bs):
            # 公司名称
            try:
                company_name = a[idx].xpath('a/@href').extract()[0]
            except:
                self.log(u'', level=log.DEBUG)
                yield None

            for brand_model in b.xpath('*'):
                # 品牌
                curr_brand_name = None
                if brand_model.extract().startswith('<span'):
                    try:
                        brand_name = brand_model.xpath('a/text()').extract()[0]
                        brand_slug = brand_model.xpath('a/@href').extract()[0]
                    except:
                        self.log(u'', level=log.ERROR)
                        yield None
                    else:
                        if u'集团' in company_name or u'汽车' in company_name:
                            company_name = company_name.strip(u'集团')
                        p_item = BrandModelItem()
                        p_item['domain'] = 'hx2car.com'
                        p_item['parent'] = brand_name.strip()
                        curr_brand_name = p_item['parent']
                        p_item['slug'] = brand_slug.strip().strip('/').split('/')[-1]
                        p_item['url'] = brand_slug.strip()
                        p_item['name'] = None
                        yield p_item
                elif brand_model.extract().startswith('<a'):
                    try:
                        model_name = brand_model.xpath('text()').extract()[0]
                        model_slug = brand_model.xpath('@href').extract()[0]
                    except:
                        self.log(u'', level=log.ERROR)
                        yield None
                    else:
                        item = BrandModelItem()
                        item['domain'] = 'hx2car.com'
                        item['parent'] = curr_brand_name
                        item['slug'] = model_slug.strip().strip('/').split('/')[-1]
                        item['url'] = model_slug.strip()
                        item['name'] = model_name
                        yield item


