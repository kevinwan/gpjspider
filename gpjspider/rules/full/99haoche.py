# -*- coding: utf-8 -*-
"""
99好车 优质二手车 规则
"""
from gpjspider.utils.constants import SOURCE_TYPE_SELLER
from .utils import *

_has = lambda x: has(x, '/..')

item_rule = {
    "class": "UsedCarItem",
    "fields": {
        'title': {
            'xpath': (
                text(has_cls('car-particular-right', '/h2/a')),
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
                _has(u'车身颜色'),
                #u'//li/span[contains(text(), "车身颜色")]/../text()',
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
                u'//*[@id="carDetailDiv"]/div[2]/ul[1]/li[4]/text()',
                text(id_('carDetailDiv', '/div[2]/ul[1]/li[4]')),
            ),
        },
        'model_slug': {
            'xpath': (
                u'//*[@id="carDetailDiv"]/div[2]/ul[1]/li[4]/text()',
                text(id_('carDetailDiv', '/div[2]/ul[1]/li[4]')),
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
                after_has(u'所属商家', 'a/@href', get_text=False),
                u'//span[contains(text(), "所属商家")]/following-sibling::a/@href',
            ),
        },
        'driving_license': {
            'xpath': (
                _has(u'行驶证'),
                #u'//li/span[contains(text(), "行驶证")]/../text()',
            ),
        },
        'invoice': {
            'xpath': (
                _has(u'购车发票'),
                #u'//li/span[contains(text(), "购车发票")]/../text()',
            ),
        },
        'maintenance_record': {
            'xpath': (
                _has(u'保养记录'),
                #u'//li/span[contains(text(), "保养记录")]/../text()',
            ),
        },
         'quality_service': {
             'xpath': [
                 has_attr2(u'质保承诺', 'title'),
                 has_attr2(u'退换承诺', 'title'),
             ],
             'processors': ['join'],
         },
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
                _has(u'交强险'),
                #u'//li/span[contains(text(), "交强险到期时间")]/../text()',
            ),
        },
        'business_insurance': {
            'xpath': (
                _has(u'商业险'),
                #u'//li/span[contains(text(), "商业险到期时间")]/../text()',
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
                _has(u'是否一手车'),
                #u'//li/span[contains(text(), "是否一手车")]/../text()',
            ),
        },
        'source_type': {
            'default': SOURCE_TYPE_SELLER,
        },
        'car_application': {
            'xpath': (
                _has(u'使用性质'),
                #u'//li/span[contains(text(), "使用性质")]/../text()',
            ),
        },
        'condition_level': {
            'xpath': [
                text(cls('rank-ico')),
                hidden('uploadid'),             # 构造链接请求服务器对应的 level 时，需要carid
            ],
            'processors': ['99haoche.condition_level']
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
        #'http://www.99haoche.com/car/4173771.html',
        #'http://www.99haoche.com/car/4483842.html',
        #'http://www.99haoche.com/car/4473155.html',
    ],

    'parse': parse_rule,

    'parse_detail': {
        "item": item_rule,
    }
}

fmt_rule_urls(rule)
#rule['parse'] = rule['parse_detail']
