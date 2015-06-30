# -*- coding: utf-8 -*-
from .utils import *

_has = lambda x: has(x, '/..')

item_rule = {
    "class": "UsedCarItem",
    "fields": {
        'title': {
            'xpath': (
                text(has_cls('title-name')),
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
                _has(u'上牌时间'),
            ),
        },
        'month': {
            'xpath': (
                _has(u'上牌时间'),
            ),
        },
        'time': {
            'xpath': (
                text(cls('f10 pr-5')),
            ),
        },
        'mile': {
            'xpath': (
                u'//*[@class="iNew-km"]//i[@class="arial fc-org f16"]/text()',
            ),
            'processors': ['first', 'ganji.mile'],
        },
        'volume': {
            'xpath': (
            ),
            'default': '%(title)s',
        },

        'color': {
            'xpath': (
                _has(u'车身颜色'),
            ),
        },
        'control': {
            'xpath': (
                _has(u'变 速 箱'),
            ),
        },
        'price': {
            'xpath': (
                text(cls('arial fc-org f20')),
            ),
        },
        'price_bn': {
            'xpath': (
                u'//*[@class="fc-org"]/i[@class="arial"]/text()',
            ),
        },
        'brand_slug': {
            'xpath': [
                text(cls('crumbs clearfix', '/a[4]')),
                text(has_cls('title-name')),
            ],
            'processors': ['ganji.brand_slug'],
        },
        'model_slug': {
            'xpath': [
                text(cls('crumbs clearfix', '/a[4]')),
                text(has_cls('title-name')),
            ],
            'processors': ['ganji.model_slug'],
        },
        'city': {
            'xpath': (
                u'//a[@class="fc-70"]/text()',
            ),
        },
        'region': {
            'xpath': (
            ),
        },
        'phone': {
            'xpath': (
                text(cls('telephone')),
            ),
            'processors': ['first', 'ganji.phone'],
        },
        'contact': {
            'xpath': (
                _has(u'联系人'),
            ),
            'processors': ['first', 'ganji.contact'],
        },
        'company_name': {
            'xpath': (
                text(cls('certdl-det', '/p/a/b')),
            ),
        },
        'company_url': {
            'xpath': (
                has_attr2(u'进入店铺', 'href'),
            ),
        },
        #'driving_license': {
            #'xpath': (
            #),
        #},
        #'invoice': {
            #'xpath': (
                #_has(u'购车发票'),
            #),
        #},
        'maintenance_record': {
            'xpath': (
                _has(u'保养方式'),
            ),
        },
         #'quality_service': {
             #'xpath': (
             #},
         #},
        'is_certifield_car': {
            'default': False,
        },
        'description': {
            'xpath': (
                text(cls('font-c-type', '/p')),
            ),
            'processors': ['souche.strip_and_join'],
        },
        'imgurls': {
            'xpath': (
                attr(cls('pics-s', '//img'), 'src'),
            ),
            'processors': ['join'],
        },
        'mandatory_insurance': {
            'xpath': (
                _has(u'交强险到期'),
            ),
        },
        'business_insurance': {
            'xpath': (
                _has(u'商业险'),
            ),
        },
        'examine_insurance': {
            'xpath': (
                _has(u'年检到期'),
            ),
        },
        'transfer_owner': {
            'xpath': (
                text(cls('arial fc-org f16')),
            ),
            'processors': ['ganji.transfer_owner'],
        },
        'source_type': {
            'default': '%(contact)s',
            'processors': ['ganji.source_type'],
        },
        'car_application': {
            'xpath': (
                _has(u'使用性质'),
            ),
        },
        'condition_level': {
            'xpath':(
            ),
        },
    },
}

parse_rule = {
    "url": {
        "re": (
            r'http://\w+\.ganji\.com/ershouche/\d+x\.htm',
        ),
        "step": 'parse_detail',
    },
    "next_page_url": {
        "xpath": (
            url(has_cls('listtab', '/')),
            '//*[@class="next"]/@href',
        ),
        #'format': 'http://www.ganji.com{0}',
        'format': True,
        "step": 'parse',
        # 'incr_pageno': 3,
    },
}


rule = {
    'name': u'赶集二手车',
    'domain': 'ganji.com',
    'base_url': 'http://www.ganji.com',
    'spider': {
        'domain': 'ganji.com',
        'download_delay': 2.5,
    },
    'start_urls': [
        'http://www.ganji.com/ershouche/',
        # 'http://www.ganji.com/ershouche/o10/',
        #'http://su.ganji.com/ershouche/1466078402x.htm', # 无新车价
        #'http://bj.ganji.com/ershouche/1696082564x.htm', # 商家正常
        #'http://tj.ganji.com/ershouche/1706909585x.htm', # 个人
        #'http://wh.ganji.com/ershouche/1582549558x.htm', # 车型有问题
    ],

    'parse': parse_rule,

    'parse_detail': {
        "item": item_rule,
    }
}

fmt_rule_urls(rule)
#rule['parse'] = rule['parse_detail']
