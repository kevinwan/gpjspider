# -*- coding: utf-8 -*-
"""
赶集好车 优质二手车
"""
import scrapy
from scrapy import log
from scrapy.http import Request
from scrapy.contrib.loader.processor import Join, TakeFirst
from scrapy.contrib.loader import ItemLoader
from gpjspider.items import UsedCarItem


class HighQualityCarHaoche51Spider(scrapy.Spider):
    """
    """
    name = "high_quality_car_ganji"
    allowed_domains = ["haoche.ganji.com"]
    start_urls = (
        'http://haoche.ganji.com',
    )
    city_dict = {}

    def parse(self, response):
        base_rule = '//ul/li/a'
        check = False
        for a in response.xpath(base_rule):
            check = True
            url = a.xpath('@href').extract()[0]
            city = a.xpath('text()').extract()[0]
            self.city_dict[url.strip('/')] = city
            url = self.start_urls[0] + url + 'buy/'
            yield Request(url, callback=self.parse_listpage)
        if not check:
            self.log(u'基本规则出错：{0}：{1}'.format(base_rule, response.url))
            yield None

    def parse_listpage(self, response):
        """
        """
        base_rule = '//ul[@class="list-bigimg clearfix"]/li/div/a/@href'
        urls = response.xpath(base_rule).extract()
        if not urls:
            m = u'parse_listpage:基本规则出错:{0}:{1}'.format(base_rule, response.url)
            self.log(m, log.ERROR)
            yield None
        for url in urls:
            if self.start_urls[0] not in url:
                _url = self.start_urls[0] + url
            else:
                _url = url
            yield Request(_url, callback=self.parse_detail)

    def parse_detail(self, response):
        """
        time   color   business_insurance
        """
        loader = ItemLoader(UsedCarItem(), response=response)
        loader.add_xpath('title', '//div[@class="dt-titbox"]/h1/text()')
        loader.add_xpath('meta', '//meta[@name="description"]/@content')
        loader.add_xpath('year', u'//li[contains(text(), "上牌时间")]/b/text()')
        loader.add_xpath('month', u'//li[contains(text(), "上牌时间")]/b/text()')
        loader.add_xpath('mile', u'//li[contains(text(), "行驶里程")]/b/text()')
        loader.add_xpath('volume', u'//li[text()="排量"]/b/text()')
        loader.add_xpath('control', u'//li[text()="变速箱"]/b/text()')
        loader.add_xpath('price', '//div[@class="pricebox"]/span/b/text()')

        loader.add_xpath(
            'price_bn',
            '//div[@class="pricebox"]/span[@class="f14"]/text()',
            TakeFirst()
        )
        loader.add_xpath(
            'brand_slug', '//div[@class="detecttitle"]/span[2]/text()'
        )
        loader.add_xpath(
            'model_slug', '//div[@class="detecttitle"]/span[2]/text()'
        )
        loader.add_xpath(
            'region', '//li[@class="owner"]/text()[4]'
        )
        loader.add_xpath(
            'description', '//p[@class="f-type03"]/text()', Join(' ')
        )
        loader.add_xpath(
            'thumbnail', '//div[@class="dt-pictype"]/img[1]/@data-original'
        )
        loader.add_xpath(
            'imgurls', '//div[@class="dt-pictype"]/img/@data-original',
            Join('###')
        )
        loader.add_xpath('phone', '//span[@class="f18"]/b/text()')
        loader.add_xpath('mandatory_insurance', '//li[@class="baoxian"]/text()')
        loader.add_xpath('examine_insurance', '//li[@class="nianjian"]/text()')
        loader.add_xpath('transfer_owner', '//li[@class="guohu"]/text()')
        loader.add_xpath(
            'condition_detail', '//div[@class="detect-txt"]/text()'
        )
        loader.add_xpath(
            'quality_service', '//ul[@class="indem-ul"]/li/p[@class]/text()',
            Join(' ')
        )
        item = loader.load_item()
        item['url'] = response.url
        item['city_slug'] = self.get_city_slug(response)
        item['city'] = self.get_city(item['city_slug'])
        item['contact'] = u'赶集好车'
        item['company_name'] = u'赶集好车'
        item['company_url'] = item['url'] = response.url
        item['is_certifield_car'] = True
        item['condition_level'] = None
        item['car_application'] = u'非营运'
        item['driving_license'] = None
        item['driving_license'] = None
        item['invoice'] = None
        item['dmodel'] = item['title']
        yield item

    def get_city_slug(self, response):
        """
        """
        _ = response.url.strip().split('/')
        if _[3] in self.city_dict:
            return _[3]
        else:
            return None

    def get_city(self, city_slug):
        """
        """
        if city_slug in self.city_dict:
            return self.city_dict[city_slug]
        else:
            return None
