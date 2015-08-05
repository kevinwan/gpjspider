# -*- coding: utf-8 -*-
"""
    iautos 第一车网
"""
from gpjspider.utils.constants import *
from .utils import *
from scrapy.http.response.text import TextResponse

_has = lambda x: has(x, '/..')

item_rule = {
    "class": "UsedCarItem",
    "fields": {
        'title': {
            'xpath': (
                text(cls('title clearfix', '/b')),
            ),
            'required': True,
        },
        'meta': {
            'xpath': (
                '//meta[@name="description" or @name="Description"]/@content',
            ),
        },
        'dmodel': {
            'defaut': '%(title)s',
        },
        'year': {
            'xpath': (
                after_has(u'首次上牌'),
            ),
            'regex': u'(\d{4})年',
            'regex_fail': None,
        },
        'month': {
            'xpath': (
                after_has(u'首次上牌'),
            ),
            'regex': u'(\d{1,2})月',
            'regex_fail': None,
        },
        'time': {
            'xpath': (
                has(u'更新'),
            ),
            'regex': r'(\d+-\d+-\d+)',
        },
        'mile': {
            'xpath': (
                after_has(u'关键参数'),
            ),
        },
        'volume': {
            'xpath': (
                after_has(u'关键参数'),
            ),
        },
        'color': {
            'xpath': (
                has(u'车身颜色', '/..'),
            ),
        },
        'control': {
            'xpath': (
                after_has(u'关键参数'),
            ),
            'regex': u'([手自]{1,2}一?[动体])',
            'regex_fail': None,
        },
        'price': {
            'xpath': (
                text(cls('price')),
            ),
        },
        'price_bn': {
            'xpath': (
                after_has(u'同款新车参考价'),
            ),
        },
        'brand_slug': {
            'xpath': (
                has(u'生产厂家', '/..'),
            ),
        },
        'model_slug': {
            'xpath': (
                after_has(u'品牌车系'),
            ),
        },
        'model_url': {
            'xpath': (
                href(cls('glb-breadcrumb', '/a[3]')),
            ),
        },
        #'status': {
            #'xpath': (
                #attr(cls('details_one', '/strong/img'), 'src'),
            #),
            #'processors': ['first', 'xcar.status'],
            #'default': 'Q',
        #},
        'city': {
            'xpath': (
                #'//meta[@name="location"]/@content',
                text(cls('glb-breadcrumb', '/a[2]')),
            ),
            #'regex': u'city=(.*);',
            'regex': u'(.*?)二手车',
        },
        'region': {
            'xpath': (
                after_has(u'看车地址'),
            ),
        },
        'phone': {
            'xpath': (
                has(u'预约电话', '/span[1]'),
            ),
        },
        'contact': {
            'xpath': (
                has(u'预约电话', '/span[2]'),
            ),
        },
        'company_name': {
            'xpath': (
                #after_has(u'门店', 'a'),
                after_has(u'经销商信息', '*/p/a'),
            ),
        },
        'company_url': {
            'xpath': (
                #u'//*[contains(text(), "门店")]/following-sibling::a/@href',
                u'//*[contains(text(), "经销商信息")]/following-sibling::*/p/a/@href',
            ),
        },
        'driving_license': {
            'xpath': (
                has(u'行驶证', '/..'),
            ),
            'processors': ['first', 'iautos.has_or_not'],
            'default': u'无',
        },
        'invoice': {
            'xpath': (
                has(u'购车发票', '/..'),
            ),
            'processors': ['first', 'iautos.has_or_not'],
            'default': u'无',
        },
        'maintenance_record': {
            'xpath': (
                has(u'保养记录', '/..'),
            ),
            'processors': ['first', 'iautos.has_or_not'],
            'default': u'无',
        },
        'quality_service': {
            'xpath': (
                attr(cls('summary-special', '/i'), 'title'),
            ),
            'processors': ['iautos.quality_service'],
        },
        'description': {
            'xpath': (
                after_has(u'卖家附言'),
            ),
        },
        'imgurls': {
            'xpath': (
                attr(cls('lazy img-center-three'), 'data-original'),
            ),
            'processors': ['join'],
        },
        'mandatory_insurance': {
            'xpath': (
                has(u'交强险', '/..'),
            ),
        },
        'business_insurance': {
            'xpath': (
                _has(u'商业险'),
            ),
        },
        #'examine_insurance': {
            #'xpath': (
                #has(u'年检情况', '/..'),
            #),
        #},
        'transfer_owner': {
            'xpath': (
                has(u'是否一手车', '/..'),
            ),
        },
        'is_certifield_car': {
            'xpath': (
                has(u'是否认证', '/..'),
            ),
            'processors': ['first', 'iautos.is_certifield_car'],
            'default': False,
        },
        'source_type': {
            'xpath': [
                has(u'是否认证', '/..'),
                after_has(u'经销商信息', '*/p/a'),
            ],
            'processors': ['iautos.source_type'],
        },
        'car_application': {
            'xpath': (
                has(u'原车用途', '/..'),
            ),
        },
        #'condition_level': {
            #'xpath':(
            #),
        #},
        #'condition_detail': {
            #'xpath': (
                #has(u'准新车'),
            #),
        #},
    },
}

parse_rule = {
    'replace': (
        {'headers': {'Content-Type': ['text/html;charset=UTF-8']}},
        {'cls': TextResponse},
    ),
    'url': {
        're': (
            r'http://www\.iautos\.cn/usedcar/\d+\.html',
        ),
        #'format': True,
        'step': 'parse_detail',
        'update': True,
        'category': 'usedcar'
    },
    'next_page_url': {
        "xpath": (
            has_attr2(u'下一页', 'href'),
        ),
        'format': True,
        'step': 'parse',
        # 'incr_pageno': 3,
    },
}


rule = {
    'name': u'第一车网',
    'domain': 'iautos.cn',
    'base_url': 'http://so.iautos.cn',
    'spider': {
        'domain': 'iautos.cn',
        'download_delay': 2.5,
    },
    'start_urls': [
        'http://so.iautos.cn/quanguo/pasdsvepcatcp1bnscac/', # 全国、只看有图
        # 'http://www.iautos.cn/usedcar/4852558.html',
        #'http://www.iautos.cn/usedcar/4812772.html', # 个人
        #'http://www.iautos.cn/usedcar/4833120.html', # 商户
        #'http://www.iautos.cn/usedcar/4638738.html', # 认证，有保证信息的车，厂家认证
        #'http://www.iautos.cn/usedcar/4826181.html', # 认证车，但是无厂家认证
    ],

    'parse': parse_rule,

    'parse_detail': {
        "item": item_rule,
    }
}

fmt_rule_urls(rule)
# rule['parse'] = rule['parse_detail']
