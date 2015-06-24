# -*- coding: utf-8 -*-
from gpjspider.utils.constants import SOURCE_TYPE_SELLER
from .utils import *

item_rule = {
    "class": "UsedCarItem",
    "fields": {
        'title': {
            'xpath': (
                #'//h1[@class="dt-titletype"]/text()',
                text(cls('dt-titletype')),
            ),
            'required': True,
        },
        'meta': {
            'xpath': (
                '//meta[@name="description" or @name="Description"]/@content',
            ),
        },
        'year': {
            'xpath': (
                #'//li[@class="one"]/b/text()',
                text(cls('one', '/b')),
            ),
        },
        'month': {
            'xpath': (
                #'//li[@class="one"]/b/text()',
                text(cls('one', '/b')),
            ),
            'default': '%(year)s',
        },
        'mile': {
            'xpath': (
                # u'//li[contains(text(), "里程")]/b/text()',
                has(u'里程', '/b'),
            ),
        },
        'volume': {
            'xpath': (
                # u'//li[contains(text(), "排量")]/b/text()',
                has(u'排量', '/b'),
            ),
        },
        'control': {
            'xpath': (
                # u'//li[contains(text(), "变速箱")]/b/text()',
                has(u'变速箱', '/b'),
            ),
        },
        'price': {
            'xpath': (
                #'//b[@class="f30 numtype"]/text()',
                text(cls('f30 numtype')),
            ),
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
                #'//b[@class="teltype"]/text()',
                text(cls('teltype')),
            ),
        },
        'brand_slug': {
            'xpath': (
                # u'//span[contains(text(), "检测车型")]/text()',
                has(u'检测车型'),
            ),
            'processors': ['first', 'ganjihaoche.brand_slug'],
        },
        'model_slug': {
            'xpath': (
                # u'//span[contains(text(), "检测车型")]/text()',
                has(u'检测车型'),
            ),
            'processors': ['first', 'ganjihaoche.model_slug'],
        },
        'city': {
            'xpath': (
                #'//a[@class="choose-city"]/span/text()',
                text(cls('choose-city', '/span')),
            ),
        },
        #'city_slug': {
            #'xpath': (
                #'//a[@class="toindex"]/@href',
                # attr(cls('toindex'), 'href'),
            #),
            #'processors': ['first', 'ganjihaoche.city_slug'],
        # },
        'region': {
            'xpath': (
                text(id_('base', '/ul/li[1]')),
            ),
            'processors': ['last']
        },
        'description': {
            'xpath': (
                #'//p[@class="f-type03"]/text()',
                text(cls('f-type03')),
            ),
        },
        'imgurls': {
            'xpath': (
                #'//div[@class="dt-pictype"]/img/@data-original',
                attr(cls('dt-pictype', '/img'), 'data-original'),
            ),
            'processors': ['join', 'strip'],
        },
        'condition_detail': {
            'xpath': [
                text(id_('accident', '/span[2]')),
                text(id_('surface', '/span[2]')),
                text(id_('system', '/span[2]')),
                text(id_('drive', '/span[2]')),
            ],
            'processors': ['join'],
        },
        'mandatory_insurance': {
            'xpath': (
                #'//li[@class="baoxian"]/text()',
                text(cls('baoxian')),
            ),
        },
        'examine_insurance': {
            'xpath': (
                #'//li[@class="nianjian"]/text()',
                text(cls('nianjian')),
            ),
        },
        'transfer_owner': {
            'xpath': (
                #'//li[@class="guohu"]/text()',
                text(cls('guohu')),
            ),
            'default': 0,
        },
        'quality_service': {
            'xpath': (
                has(u'质保', prefix=cls('f-type01', '')),
                # has(u'质保', prefix=cls('f-type01', '//')),
                # '//ul[@class="indem-ul"]/li/p[@class]/text()',
            ),
        },
        'is_certifield_car': {
            'default': 1,
            'default': '%(quality_service)s',
        },
        'source_type': {
            'default': SOURCE_TYPE_SELLER,
        },
    },
}

parse_rule = {
    "url": {
        "xpath": (
            url(has_cls('list-infoBox')),
        ),
        "format": "http://haoche.ganji.com{0}",
        "step": 'parse_detail',
        'update': True,
        'category': 'usedcar',
    },
    "next_page_url": {
        "xpath": (
            '//a[@class="next"]/@href',
        ),
        "format": "http://haoche.ganji.com{0}",
        "step": 'parse',
        # 'incr_pageno': 10,
    },
}

rule = {
    'name': u'赶集好车',
    'domain': 'haoche.ganji.com',
    'start_urls': [
        'http://haoche.ganji.com/www/buy/',
        # 'http://haoche.ganji.com/cn/buy/o2/',
        # 'http://haoche.ganji.com/cc/1713365366x.htm',
    ],

    'parse': parse_rule,

    'parse_detail': {
        "item": item_rule,
    },
}
# rule['parse'] = rule['parse_detail']