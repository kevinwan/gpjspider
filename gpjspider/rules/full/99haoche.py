# -*- coding: utf-8 -*-
"""
99好车 优质二手车 规则
"""
from gpjspider.utils.constants import SOURCE_TYPE_SELLER
from .utils import *

item_rule = {
    "class": "UsedCarItem",
    "fields": {
        'title': {
            'xpath': (
                text(has_cls('car-particular-right', '/h2/a')),
                text('//title'),
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
                #u'//li/span[contains(text(), "首次上牌")]/../span[@class="righ"]/text()',
                text(cls('date', '/ul/li[1]')),
            ),
        },
        'month': {
            'xpath': (
                #u'//li/span[contains(text(), "首次上牌")]/../span[@class="righ"]/text()',
                text(cls('date', '/ul/li[1]')),
            ),
            #'default': '%(year)s',
        },
        'mile': {
            'xpath': (
                #u'//div[@class="date"]/ul/li[2]/text()',
                text(cls('date', '/ul/li[2]')),
            ),
        },
        'volume': {
            'xpath': (
            ),
            'default': '%(title)s',
        },

        'color': {
            'xpath': (
                #u'//li/span[contains(text(), "车身颜色")]/../text()',
                has(u'车身颜色', '/..'),
            ),
        },
        'control': {
            'xpath': (
                #u'//*[@id="carDetailDiv"]/ul/li[2]/text()',
                text(id_('carDetailDiv', '/ul/li[2]')),
            ),
        },
        'price': {
            'xpath': (
                #text(cls('num')),
                text(cls('price', '/span[1]')),
                #u'//div[@class="price"]/span[1]/text()',
            ),
            'processors': ['join'],
        },
        'price_bn': {
            'xpath': (
                #text(cls('txt')),
                text(cls('price', '/span[2]')),
                #'//p[@class="market-price"]/del/text()',
            ),
        },
        'brand_slug': {
            'xpath': (
                #u'//*[@id="carDetailDiv"]/div[2]/ul[1]/li[4]/text()',
                text(id_('carDetailDiv', '/div[2]/ul[1]/li[4]')),
            ),
        },
        'model_slug': {
            'xpath': (
                text(id_('carDetailDiv', '/div[2]/ul[1]/li[4]')),
                #u'//*[@id="carDetailDiv"]/div[2]/ul[1]/li[4]/text()',
            ),
        },
        'city': {
            'xpath': (
                #u'//h2[@name="location"]/a[2]/text()',
                text('h2[@name="location"]/a[2]'),
            ),
        },
        'region': {
            'xpath': (
                #u'//p[@class="car-site"]/text()',
                text(cls('car-site')),
            ),
            'processors': ['last'],
        },
        'phone': {
            'xpath': (
                hidden('uploadid'),
            ),
            'processors': ['first', '99haoche.phone']
        },
        'company_name': {
            'xpath': (
                #u'//span[contains(text(), "所属商家")]/following-sibling::a/text()',
                after_has(u'所属商家'),
            ),
        },
        'company_url': {
            'xpath': (
                u'//span[contains(text(), "所属商家")]/following-sibling::a/@href',
            ),
        },
        'driving_license': {
            'xpath': (
                #u'//li/span[contains(text(), "行驶证")]/../text()',
                has(u'行驶证', '/..'),
            ),
        },
        'invoice': {
            'xpath': (
                #u'//li/span[contains(text(), "购车发票")]/../text()',
                has(u'购车发票', '/..'),
            ),
        },
        'maintenance_record': {
            'xpath': (
                #u'//li/span[contains(text(), "保养记录")]/../text()',
                has(u'保养记录', '/..'),
            ),
        },
        # 'quality_service': {
        #     'xpath': (
        #         u'//div[@class="diverse-serve"]/p/a/text()',
        #     ),
        #     'processors': ['join', 'strip'],
        # },
        'is_certifield_car': {
            'default': 1,
        },
        'description': {
            'xpath': (
                '//div[@class="postscript"]/p[1]/text()',
            ),
        },
        'imgurls': {
            'xpath': (
                #'//ul[@id="img_R_L_List"]/li/a/img/@src',
                attr(id_('img_R_L_List', '/li/a/img'), 'src'),
            ),
            'processors': ['join'],
        },
        'mandatory_insurance': {
            'xpath': (
                #u'//li/span[contains(text(), "交强险到期时间")]/../text()',
                has(u'交强险', '/..'),
            ),
        },
        'business_insurance': {
            'xpath': (
                #u'//li/span[contains(text(), "商业险到期时间")]/../text()',
                has(u'商业险', '/..'),
            ),
        },
        'examine_insurance': {
            'xpath': (
                #u'//td[contains(text(), "年检有效期")]/following-sibling::td/text()',
                after_has(u'年检有效期'),
            ),
        },
        'transfer_owner': {
            'xpath': (
                #u'//li/span[contains(text(), "是否一手车")]/../text()',
                has(u'是否一手车', '/..'),
            ),
        },
        'source_type': {
            'default': SOURCE_TYPE_SELLER,
        },
        'car_application': {
            'xpath': (
                #u'//li/span[contains(text(), "使用性质")]/../text()',
                has(u'使用性质', '/..'),
            ),
        },
        # maintenance_desc
    },
}

parse_rule = {
    "url": {
        "re": (
            r'http://www\.99haoche\.com/car/\d+\.html',
        ),
        "step": 'parse_detail',
        'update': True,
        'category': 'usedcar'
    },
    "next_page_url": {
        "xpath": (
            '//a[@id="pagenow"]/following-sibling::a[1]/@href',
        ),
        'format': 'http://www.99haoche.com{0}',
        "step": 'parse',
        # 'incr_pageno': 3,
    },
}


rule = {
    'name': u'99好车',
    'domain': '99haoche.com',
    'start_urls': [
        'http://www.99haoche.com/quanguo/all/?p=v1',
        #'http://www.99haoche.com/car/4486289.html',
    ],

    'parse': parse_rule,

    'parse_detail': {
        "item": item_rule,
    }
}

fmt_rule_urls(rule)
#rule['parse'] = rule['parse_detail']
