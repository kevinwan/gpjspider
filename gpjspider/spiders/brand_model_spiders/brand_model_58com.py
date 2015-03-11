# -*- coding: utf-8 -*-
import json
import traceback
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
    # 车系 URL 模板
    model_url_template = (
        "http://api.58.com/comm/cmcs/all/all/cityid-5/cateid-29/?api_marktar"
        "get=false&api_listname={brand}&api_retparameterid=5867&api_type=json")

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
                    item['parent'] = j['text'].strip()
                    if u'不限' in item['parent']:
                        continue
                    item['url'] = j['url'].strip()
                    item['domain'] = '58.com'
                    item['slug'] = item['url'].strip().strip('/').split('/')[-1]

                    model_url = self.model_url_template.format(brand=item['slug'])
                    request = Request(model_url, self.parse_model)
                    request.meta['item'] = item
                    yield request

    def parse_model(self, response):
        """
        """
        json_str = response.body_as_unicode()
        try:
            j = json.loads(json_str)
            ms = j['comms_getcmcsinfo'][0]['allpropertys']
            ms = ms['allproperty'][0]['propertyvalues']
        except:
            s = traceback.format_exc()
            self.log(u'json 异常：\n{0}'.format(s), level=log.ERROR)
        else:
            for m in ms:
                try:
                    model_name = m['text'].strip()
                    slug = m['listname'].strip()
                except:
                    continue
                item = deepcopy(response.meta['item'])
                item['name'] = model_name
                item['url'] = 'http://quanguo.58.com/' + slug
                item['slug'] = slug
                yield item
        item = response.meta['item']
        item['name'] = item['parent']
        item['parent'] = None
        yield item
