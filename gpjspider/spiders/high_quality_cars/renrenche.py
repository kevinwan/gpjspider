# -*- coding: utf-8 -*-
"""
人人车 优质二手车
"""
import traceback
import scrapy
from scrapy import log
from scrapy.http import Request
from scrapy.contrib.loader.processor import Join, TakeFirst
from scrapy.contrib.loader import ItemLoader
from gpjspider.items import UsedCarItem
from gpjspider.utils import constants


class HighQualityCarRenRenCheSpider(scrapy.Spider):
    """
    maintenance_record  无法获取此字段
    time 无法发现页面发布时间标示，
    color
    maintenance_desc  保养信息
    """
    name = "high_quality_car_renrenche"
    allowed_domains = ["renrenche.com"]
    start_urls = (
        "http://www.renrenche.com/bj/ershouche",
        "http://www.renrenche.com/sz/ershouche",
        "http://www.renrenche.com/gz/ershouche",
        "http://www.renrenche.com/nj/ershouche",
        "http://www.renrenche.com/cd/ershouche",
        "http://www.renrenche.com/dg/ershouche",
        "http://www.renrenche.com/cq/ershouche",
        "http://www.renrenche.com/wei/ershouche",
        "http://www.renrenche.com/suz/ershouche",
        "http://www.renrenche.com/wh/ershouche",
        "http://www.renrenche.com/sh/ershouche",
    )

    city_dict = {
        'gz': u'广州',
        'bj': u'北京',
        'sz': u'深圳',
        'nj': u'南京',
        'cd': u'成都',
        'dg': u'东莞',
        'cq': u'重庆',
        'wh': u'武汉',
        'sh': u'上海',
        'wei': u'威海',
        'suz': u'苏州'
        }

    def parse(self, response):
        """
        """
        url_rule = '//div[@class="container search-list-wrapper"]/ul/li/a/@href'
        urls = response.xpath(url_rule)
        if not urls:
            self.log(u'基本规则失效：{0}'.format(response.url), log.ERROR)
            yield None
        else:
            for url in urls:
                _url = url.extract()
                if 'http' not in _url:
                    _url = 'http://www.renrenche.com' + _url
                yield Request(_url, callback=self.parse_detail)

    def parse_detail(self, response):
        """
        """
        loader = ItemLoader(UsedCarItem(), response=response)
        loader.add_xpath('title', '//div[@id="basic"]/div/div/h1/text()')
        loader.add_xpath('meta', '//meta[@name="description"]/@content')
        loader.add_xpath('year', u'//div[@class="history-event"]/p[contains(text(), "首次上牌")]/following-sibling::p/text()')
        loader.add_xpath('month', u'//div[@class="history-event"]/p[contains(text(), "首次上牌")]/following-sibling::p/text()')
        loader.add_xpath('mile', '//div[@class="detail-box"]/ul/li[2]/p/strong/text()')
        loader.add_xpath('volume', u'//div[@class="span7"]//tr/td[text()="发动机"]/../td[@class]/text()')
        loader.add_xpath('color', u'//td[text()="车身颜色"]/following-sibling::td[1]/text()')
        loader.add_xpath('control', u'//div[@class="span7"]//tr/td[text()="变速箱"]/../td[@class]/text()')
        loader.add_xpath('price', '//p[@class="box-price"]/text()')
        loader.add_xpath('brand_slug', '//ul[@class="box-installment block-height"]/li/text()')
        loader.add_xpath('price_bn', '//li[@id="box_installment"]/following-sibling::li/text()')
        loader.add_xpath('region', '//p[@class="owner-info"]/text()[2]')
        loader.add_xpath(
            'description', '//div[@class="text-block bottom-right"]/p/text()',
            TakeFirst()
        )
        loader.add_xpath('thumbnail', '//div[@class="detail-box-bg"]/img/@src')
        loader.add_xpath(
            'imgurls',
            '//div[@class="container detail-gallery"]/div/div/div/div/img/@src',
            Join('###')
        )

        loader.add_xpath('phone', '//span[@class="tel"]/text()[2]')
        loader.add_xpath(
            'mandatory_insurance',
            u'//td[contains(text(), "交强险到期时间")]/following-sibling::td[1]/text()'
        )
        loader.add_xpath(
            'business_insurance',
            u'//td[contains(text(), "商业险到期时间")]/following-sibling::td[1]/text()'
        )
        loader.add_xpath(
            'examine_insurance',
            u'//td[contains(text(), "年检到期时间")]/following-sibling::td[1]/text()'
        )
        loader.add_xpath(
            'examine_insurance',
            u'//td[contains(text(), "年检到期时间")]/following-sibling::td[1]/text()'
        )
        loader.add_xpath(
            'transfer_owner',
            u'//td[contains(text(), "过户次数")]/following-sibling::td[1]/text()'
        )
        loader.add_xpath(
            'condition_level',
            u'//p[@class="top-banner"]/span[@class="desc"]/text()',
            TakeFirst()
        )

        loader.add_xpath(
            'condition_detail',
            u'//p[@class="top-banner"]/span[@class="desc"]/text()',
            Join(' ')
        )

        loader.add_xpath(
            'maintenance_record',
            u'//td[contains(text(), "是否4S店保养")]/following-sibling::td[1]/text()'
        )

        loader.add_xpath(
            'quality_service',
            u'//div[@class="container common-promise"]/div/div/div/p[@class="promise-desc"]/text()',
            Join('###')
        )
        item = loader.load_item()
        loader.add_value('contact', u'人人车')
        loader.add_value('company_name', u'人人车')
        loader.add_value('car_application', u'非运营')
        item['company_url'] = item['url'] = response.url

        item['city_slug'] = self.get_city_slug(response)
        item['city'] = self.get_city(item['city_slug'])
        yield item

        # time  无词字段
        # model_slug  从标题处   dmodel
        # city   city_slug     region_slug
        # invoice  driving_license 无法确认  maintenance_desc

    def get_city_slug(self, response):
        """
        """
        try:
            city_slug = response.url.strip().split('/')[3]
        except:
            s = traceback.format_exc()
            self.log(u'未知异常:{0}:{1}'.format(response.url, s), log.ERROR)
            return None
        else:
            if city_slug in self.city_dict:
                return city_slug
            else:
                self.log(u'未知城市:{0}:{1}'.format(city_slug, response.url))
                return None

    def get_city(self, city_slug):
        if city_slug in self.city_dict:
            return self.city_dict[city_slug]
        else:
            return None
