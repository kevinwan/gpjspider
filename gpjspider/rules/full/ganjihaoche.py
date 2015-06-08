# -*- coding: utf-8 -*-
from gpjspider.utils.constants import SOURCE_TYPE_SELLER
from .utils import *

rule = {
    #==========================================================================
    #  基本配置
    #==========================================================================
    'name': u'赶集好车',
    'domain': 'haoche.ganji.com',
    'start_urls': [
        #'http://haoche.ganji.com/cn/buy/',
        'http://haoche.ganji.com/www/buy/',
        # 'http://haoche.ganji.com/cn/buy/o2/',
    ],

    #==========================================================================
    #  默认步骤  parse
    #==========================================================================
    'parse': {
        #     "url": {
        #         "xpath": ('//div[@class="c2city"]/ul/li/a/@href',),
        #         "format": "http://haoche.ganji.com{0}buy/",
        #         "step": 'parse_list',
        #     }
        # },
        # 'parse_list': {
        "url": {
            "xpath": (
                url(has_cls('list-infoBox')),
            ),
            "format": "http://haoche.ganji.com{0}",
            "step": 'parse_detail',
            'update': True,
            'category': 'usedcar'
        },
        "next_page_url": {
            "xpath": (
                '//a[@class="next"]/@href',
            ),
            "format": "http://haoche.ganji.com{0}",
            "step": 'parse',
            # 'incr_pageno': 10,
        },
    },

    #==========================================================================
    #  详情页步骤  parse_detail
    #==========================================================================
    'parse_detail': {
        "item": {
            "class": "UsedCarItem",
            "fields": {
                'title': {
                    'xpath': (
                        '//h1[@class="dt-titletype"]/text()',
                    ),
                    'required': True,
                },
                'meta': {
                    'xpath': (
                        '//meta[@name="description"]/@content',
                        '//meta[@name="Description"]/@content',
                    ),
                },
                'year': {
                    'xpath': ('//li[@class="one"]/b/text()',),
                },
                'month': {
                    'xpath': ('//li[@class="one"]/b/text()',),
                    'default': '%(year)s',
                },
                'mile': {
                    'xpath': (u'//li[contains(text(), "里程")]/b/text()',),
                },
                'volume': {
                    'xpath': (u'//li[contains(text(), "排量")]/b/text()',),
                },
                'control': {
                    'xpath': (u'//li[contains(text(), "变速箱")]/b/text()',),
                },
                'price': {
                    'xpath': ('//b[@class="f30 numtype"]/text()',),
                },
                #  加上 price之后才是新车价
                'price_bn': {
                    'xpath': (
                        '//div[@class="pricebox"]/span[@class="f14"]/i/text()',
                    ),
                    'processors': ['first', 'ganjihaoche.price_bn'],
                },
                'phone': {
                    'xpath': (
                        '//b[@class="teltype"]/text()',
                    ),
                },
                'brand_slug': {
                    'xpath': (u'//span[contains(text(), "检测车型")]/text()',),
                    'processors': ['first', 'ganjihaoche.brand_slug'],
                },
                'model_slug': {
                    'xpath': (u'//span[contains(text(), "检测车型")]/text()',),
                    'processors': ['first', 'ganjihaoche.model_slug'],
                },
                'city': {
                    'xpath': (
                        '//a[@class="choose-city"]/span/text()',
                    ),
                },
                'city_slug': {
                    'xpath': (
                        '//a[@class="toindex"]/@href',
                    ),
                    'processors': ['first', 'ganjihaoche.city_slug'],
                },
                'description': {
                    'xpath': ('//p[@class="f-type03"]/text()',),
                },
                'imgurls': {
                    'xpath': ('//div[@class="dt-pictype"]/img/@data-original',),
                },
                'mandatory_insurance': {
                    'xpath': ('//li[@class="baoxian"]/text()',),
                },
                'examine_insurance': {
                    'xpath': ('//li[@class="nianjian"]/text()',),
                },
                'transfer_owner': {
                    'xpath': ('//li[@class="guohu"]/text()',),
                    'default': 0,
                },
                'quality_service': {
                    'xpath': (
                        '//ul[@class="indem-ul"]/li/p[@class]/text()',
                    ),
                },
                'source_type': {
                    'default': SOURCE_TYPE_SELLER,
                },
            },
        },
    },
}
