# -*- coding: utf-8 -*-
"""
抓取汽车之家的4S店
"""
from decimal import Decimal
import scrapy
from scrapy import log
from scrapy.http import Request
from gpjspider.items import FourSShopItem


class FourSShopAutohome(scrapy.Spider):
    name = "4s_shop_autohome"
    allowed_domains = ["autohome.com.cn"]
    start_urls = (
        'http://dealer.autohome.com.cn/china/',
    )

    def parse(self, response):
        """
    longitude = Field()
    latitude = Field()
        """
        rule = '//div[@id="dealer-01"]/div[contains(@class, "dealer-cont")]/div'
        shops = response.xpath(rule)
        if not shops:
            self.log(u'基本规则失效:{0}'.format(rule), log.ERROR)
            yield None
        for shop in shops:
            shop_name = shop.xpath('h3/a[not(@class)]/text()').extract()
            city = shop.xpath('h3/a[not(@class)]/@js-darea').extract()
            phone = shop.xpath('dl/dd/div/span/span/text()').extract()
            address = shop.xpath('dl/dd/div[@title]/a/../@title').extract()
            bran_rule = u'dl/dd/div[@title and contains(text(), "品牌")]/@title'
            brands = shop.xpath(bran_rule).extract()
            url = shop.xpath('dl/dd/div[@title]/a/@href').extract()
            item = FourSShopItem()
            item['domain'] = "autohome.com.cn"
            if not url:
                self.log(u'url规则失效:{0}'.format(response.url), log.ERROR)
                continue
            item['url'] = "http://dealer.autohome.com.cn" + url[0]
            if not shop_name:
                self.log(u'shop_name:{0}'.format(response.url), log.ERROR)
                continue
            item['shop_name'] = shop_name[0]
            if not city:
                self.log(u'city规则失效:{0}'.format(response.url), log.ERROR)
                continue
            item['city'] = city[0]
            if not phone:
                self.log(u'phone规则失效:{0}'.format(response.url), log.ERROR)
                continue
            item['phone'] = phone[0]
            if not address:
                self.log(u'address规则失效:{0}'.format(response.url), log.ERROR)
                continue
            item['address'] = address[0]
            if not brands:
                self.log(u'brands规则失效:{0}'.format(response.url), log.ERROR)
                continue
            item['brands'] = u"###".join(brands)
            request = Request(item['url'], callback=self.parse_4s)
            request.meta['item'] = item
            yield request
        try:
            next_url_rule = '//a[@class="page-item-next"]/@href'
            next_url = response.xpath(next_url_rule).extract()[0]
        except:
            self.log(u'获取下一页规则失效', log.ERROR)
            yield None
        else:
            next_url = 'http://dealer.autohome.com.cn' + next_url
            yield Request(next_url, callback=self.parse)

    def parse_4s(self, response):
        """
        """
        s_index = response.body.find('MapLonBaidu":') + len('MapLonBaidu":')
        e_index = response.body.find(',', s_index)
        longitude = response.body[s_index:e_index]
        s_index = response.body.find('MapLatBaidu":') + len('MapLatBaidu":')
        e_index = response.body.find(',', s_index)
        latitude = response.body[s_index:e_index]
        item = response.meta['item']
        try:
            item['longitude'] = Decimal(longitude)
            item['latitude'] = Decimal(latitude)
        except:
            msg = 'longitude：{0}, latitude:{1}'.format(longitude, latitude)
            self.log(msg, log.ERROR)
            item['longitude'] = Decimal(0)
            item['latitude'] = Decimal(0)
            yield item
        else:
            yield item
