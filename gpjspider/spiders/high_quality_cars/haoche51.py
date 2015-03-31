# -*- coding: utf-8 -*-
"""
好车无忧 优质二手车
"""
import scrapy
from scrapy import log
from scrapy.http import Request
from scrapy.contrib.loader.processor import Join
from scrapy.contrib.loader import ItemLoader
from gpjspider.items import UsedCarItem
from gpjspider.utils import constants


class HighQualityCarHaoche51Spider(scrapy.Spider):
    """
    maintenance_record  无法获取此字段
    time 无法发现页面发布时间标示，
    color
    maintenance_desc  保养信息
    """
    name = "high_quality_car_haoche51"
    allowed_domains = ["haoche51.com"]
    start_urls = (
        'http://bj.haoche51.com/vehicle_list.html',
        'http://sz.haoche51.com/vehicle_list.html',
        'http://cd.haoche51.com/vehicle_list.html',
        'http://cq.haoche51.com/vehicle_list.html',
        'http://wu.haoche51.com/vehicle_list.html',
        'http://su.haoche51.com/vehicle_list.html',
        'http://dg.haoche51.com/vehicle_list.html',
        'http://zz.haoche51.com/vehicle_list.html',
        'http://nj.haoche51.com/vehicle_list.html',
        'http://xm.haoche51.com/vehicle_list.html',
        'http://sh.haoche51.com/vehicle_list.html',
        'http://fs.haoche51.com/vehicle_list.html',
    )
    # 去重用的
    current_id = -1

    def parse(self, response):
        base_rule = '//div[@class="content"]/div/div/@onclick'
        # base_rule = '//div[@class="mc-box"]/div/@onclick'
        urls = response.xpath(base_rule)
        if not urls:
            msg = u"基本规则发生变化：{0}:{1}".format(base_rule, response.url)
            self.log(msg, log.ERROR)
            yield None
        else:
            for url in urls:
                s = url.extract()
                if not s.startswith('javascript:window.open'):
                    self.log(u'列表页有变化：{0}'.format(response.url), log.ERROR)
                    continue
                start_index = s.find('http')
                end_index = s.find('html') + len('html')
                new_url = s[start_index:end_index]
                yield Request(new_url, callback=self.parse_detail)

    def parse_detail(self, response):
        """
        """
        loader = ItemLoader(item=UsedCarItem(), response=response)
        loader.add_value('url', response.url)
        loader.add_xpath('title', '//div[@class="autotit"]/strong/text()')
        loader.add_xpath('meta', '//meta[@name="Description"]/@content')
        loader.add_xpath('year', '//div[@class="autotit"]/h2/text()')
        loader.add_xpath('month', '//div[@class="autotit"]/h2/text()')
        loader.add_xpath('mile', '//div[@class="autotit"]/h2/text()')
        loader.add_xpath('control', '//div[@class="autotit"]/h2/text()')
        loader.add_xpath(
            'transfer_owner', '//div[@class="autotit"]/h2/text()'
        )
        loader.add_xpath(
            'volume',
            (u'//div[@class="tab-list"]/ul/li[contains(text(), "排量")]'
                '/following-sibling::li[1]/text()')
        )
        loader.add_xpath('price', '//div[@class="car-quotation"]/strong/text()')
        loader.add_xpath(
            'price_bn',
            '//div[@class="car-cost"]/ul/li/i[@class="newcarj"]/text()'
        )
        loader.add_xpath(
            'brand_slug',
            '//div[@class="autotit"]/strong/text()'
        )
        loader.add_xpath(
            'region',
            '//div[@class="car-cost"]/ul/li/div[@class="thecar1"]/text()'
        )
        loader.add_xpath(
            'description',
            '//div[@class="ow-sa"]/p/text()', Join('<br>')
        )

        loader.add_xpath(
            'imgurls',
            '//div[@id="car-pic1"]/ul/li/a/img/@data-original', Join('###')
        )

        # contact 从描述中提取

        loader.add_xpath(
            'phone',
            '//div[@class="tel-consu"]/ul/li[@class="tc-der"]/strong/text()'
        )
        loader.add_xpath(
            'mandatory_insurance',
            u'//div[@class="ow-sa1"]/ul/li[contains(text(), "交强险")]/text()'
        )
        loader.add_xpath(
            'business_insurance',
            u'//div[@class="ow-sa1"]/ul/li[contains(text(), "商业险")]/text()'
        )
        loader.add_xpath(
            'examine_insurance',
            u'//div[@class="ow-sa1"]/ul/li[contains(text(), "年检")]/text()'
        )

        loader.add_xpath(
            'condition_level',
            u'//div[@class="on-car"]/i[contains(text(), "车况")]/text()'
        )

        loader.add_xpath(
            'condition_detail',
            u'//div[@class="pur-car-recom"]/p[2]/text()'
        )

        loader.add_xpath(
            'driving_license',
            u'//div[@class="ow-sa1"]/ul/li[contains(text(), "行驶证")]/text()'
        )
        loader.add_xpath(
            'invoice',
            u'//div[@class="ow-sa1"]/ul/li[contains(text(), "购车发票/过户")]/text()'
        )
        loader.add_xpath(
            'quality_service',
            u'//div[@class="z-box"]/ul/li/text()', Join(separator='###')
        )
        item = loader.load_item()

        loader.add_value('company_name', u'好车无忧')
        loader.add_value('company_url', response.url)
        loader.add_value('domain', 'haoche51.com')
        # haoche51的车源都是商家车源
        loader.add_value('source_type', constants.SOURCE_TYPE_SELLER)
        # title即原始型号
        if item.get('title'):
            item['dmodel'] = item['title']
        item['city_slug'] = self.get_city_slug(response)
        item['city'] = self.get_city(response)
        yield item

    def get_city(self, response):
        """
        """
        city_dict = {
            'cd': u'成都',
            'bj': u'北京',
            'sz': u'深圳',
            'cq': u'重庆',
            'wu': u'无锡',
            'su': u'苏州',
            'dg': u'东莞',
            'zz': u'郑州',
            'nj': u'南京',
            'xm': u'厦门',
            'sh': u'上海',
            'fs': u'佛山',
        }
        city_slug = self.get_city_slug(response)
        city = city_dict.get(city_slug)
        if not city:
            self.log(u'不存在此城市:{0}'.format(city_slug), log.ERROR)
        return city

    def get_city_slug(self, response):
        """http://cd.haoche51.com/vehicle_list.html
        """
        if response.url.startswith('https://'):
            city_slug = response.url[8:10]
        else:
            city_slug = response.url[7:9]
        self.log(u'city slug:{0}:{1}'.format(city_slug, response.url), log.INFO)
        return city_slug
