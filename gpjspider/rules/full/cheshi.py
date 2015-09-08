# -*- coding: utf-8 -*-
"""
    cheshi.com 网上车市
"""
from gpjspider.utils.constants import *
from .utils import *

_has = lambda x: has(x, '/..')

item_rule = {
    "class": "UsedCarItem",
    "fields": {
        'title': {
            'xpath': (
                text(cls('part_h3s')),
                # text(cls('f18 gray3')),
            ),
            'required': True,
        },
        'meta': {
            'xpath': (
                '//meta[@name="description" or @name="Description"]/@content',
            ),
        },
        'dmodel': {
            # 'xpath': (
            #     after_has(u'本车标签'),
            # ),
            'default': '%(title)s',
        },
        'year': {
            'xpath': (
                after_has(u'上牌时间'),
            ),
            'processors': ['cheshi.year'],
        },
        # 'month': {
        #     'xpath': (
        #         has(u'上牌时间'),
        #     ),
        # },
        'time': {
            'xpath': (
                text(cls('part_h3s', '/span')),
            ),
        },
        'mile': {
            'xpath': (
                after_has(u'行驶里程'),
            ),
            'processors': ['first', 'cheshi.mile'],
        },
        'volume': {
            'xpath': (
                has(u'排量', '/..', u'span[not(contains(text(), "暂无"))]/*'),
                has(u'排量', '/a') + '|' + text(cls('part_h3s')),
            ),
            'processors': ['cheshi.volume'],
        },
        'color': {
            'xpath': (
                '//title/text()',
            ),
            'processors': ['first', 'cheshi.color'],
        },
        'control': {
            'xpath': (
                has(u'变速箱', u'/..', u'span[not(contains(text(), "暂无"))]/*'),
                has(u'变速箱', '/a') + '|' + text(cls('part_h3s')),
            ),
            'processors': ['join', 'cheshi.control'],
            'regex': u'([手自]{1,2}一?[动体])',
            'regex_fail': None,
        },
        'price': {
            'xpath': (
                before_has(u'万元'),
            ),
        },
        # 'price_bn': {
        #     'xpath': (
        #         has(u'出厂报价', '/strong[1]'),
        #     ),
        #     'regex': '(\d+\.?\d*)',
        # },
        'brand_slug': {
            'xpath': (
                '//*[@class="sc-bread"]/a[last()-1]/text()',
            ),
            'processors': ['first', 'cheshi.brand_or_model'],
            #'regex': u'二手(.*)',
        },
        'model_slug': {
            'xpath': (
                '//*[@class="sc-bread"]/a[last()]/text()',
            ),
            'processors': ['first', 'cheshi.brand_or_model'],
            #'regex': u'二手(.*)',
        },
        'model_url': {
            'xpath': (
                '//*[@class="sc-bread"]/a[last()]/@href',
            ),
            'processors': ['first', 'cheshi.model_url'],
            'format': True,
        },
        'city': {
            'xpath': (
                #'//*[@class="sc-bread"]/a[last()-2]/text()',
                after_has(u'上牌地区', 'a[2]'),
                after_has(u'上牌地区', 'a'),
                # has(u'所在地区', '/..'),
            ),
            'before': u'地区',
            #'regex': u'(.*?)二手',
            # 'processors': ['first', 'cheshi.city'],
        },
        'region': {
            'xpath': (
                has(u'地址', '/..'),
            ),
        },
        'phone': {
            'xpath': (
                text(id_('linkaddr', '/a[@class="btn_cr_car"]')),
                href(cls('btn_cr_car')),
                has(u'电话', '/..'),
            ),
            'processors': ['cheshi.phone'],
        },
        # 'contact': {
        #     'xpath': (
        #         text(id_('linkman')),
        #     ),
        # },
        'company_name': {
            'xpath': (
                text(cls('dealer-list clearfix mt', '/p[1]/strong/a')),
            ),
        },
        'company_url': {
            'xpath': (
                href(cls('dealer-list clearfix mt', '/p[1]/strong/a')),
            ),
        },
        'driving_license': {
            'xpath': (
                has(u'行驶证', '/..'),
            ),
        },
        'invoice': {
            'xpath': (
                has(u'购车发票', '/..'),
            ),
        },
        # 'maintenance_record': {
        #     'xpath': (
        #         has(u'保养情况', '/..'),
        #     ),
        # },
        # 'quality_service': {
        #     'xpath': (
        #         attr(cls('ensure', '/a'), 'title'),
        #     ),
        #     'processors': ['join'],
        # },
        'description': {
            'xpath': (
                after_has(u'补充说明'),
            ),
        },
        'imgurls': {
            'xpath': (
                #'//*[@class="contentdiv"]//img/@src',
                '//*[@class="explain clearfix"]/following-sibling::p//@src',
                '//*[@class="dl01 clearfix"]//@src',
            ),
            'processors': ['join'],
        },
        'mandatory_insurance': {
            'xpath': (
                has(u'交强险', '/..'),
            ),
        },
        # 'business_insurance': {
        #     'xpath': (
        #         _has(u'商业险'),
        #     ),
        # },
        'examine_insurance': {
            'xpath': (
                has(u'年审到期', '/..'),
            ),
        },
        'transfer_owner': {
            'xpath': (
                has(u'过户次数'),
            ),
            'regex': u'过户次数：(.*)',
        },
        'is_certifield_car': {
            'default': 0,
        },
        'source_type': {
            'xpath': (
                text(cls('part_h3s', '/em')),
            ),
            'processors': ['first', 'cheshi.source_type'],
        },
    },
}

parse_rule = {
    'url': {
        're': (
            r'/info/\d+\.html',
        ),
        'format': True,
        'step': 'parse_detail',
    },
    'next_page_url': {
        "xpath": (
            # href(cls('sc-menu2 l', '/li/a')),
            next_page(),
        ),
        #'format': True,
        'step': 'parse',
        # 'incr_pageno': 3,
    },
}


# parse_list = {
#     'url': {
#         're': (
#             r'http://seller.cheshi.com/\d+/ersc_\d+\.html',
#         ),
#         'step': 'parse_detail',
#     },
# }


rule = {
    'name': u'网上车市',
    'domain': 'cheshi.com',
    'base_url': 'http://2sc.cheshi.com',
    # 'dealer': {
    #     'url': '%sersclist.html',
    # },
    'start_urls': [
        'http://2sc.cheshi.com/china/?order=5',  # 时间降序
        'http://2sc.cheshi.com/china/s1/?order=5',
        'http://2sc.cheshi.com/china/s2/?order=5',
        'http://2sc.cheshi.com/china/s3/?order=5',
        #'http://2sc.cheshi.com/info/1655182.html', # 网页导航栏结构有异，提取不了品牌型号
        #'http://2sc.cheshi.com/info/1655192.html', # 品牌、型号顺序反了
        #'http://2sc.cheshi.com/info/1144895.html', # 4s, 有电话
        #'http://2sc.cheshi.com/info/833448.html', # 个人，点击显示电话
        #'http://2sc.cheshi.com/info/1656434.html', # 综合、商家
        # 'http://2sc.cheshi.com/info/1523868.html',  # city is null
        # 'http://2sc.cheshi.com/info/1748470.html',  # phone is None
        # 'http://2sc.cheshi.com/info/402736.html',  # phone is None
        # 'http://2sc.cheshi.com/info/1752119.html',  # volume is None
        # 'http://2sc.cheshi.com/info/1752955.html',  # phone is None
        # 'http://2sc.cheshi.com/info/1752875.html',  # year is 0
        # 'http://2sc.cheshi.com/info/385843.html',  # control is null
        # 'http://2sc.cheshi.com/info/890163.html',  # control is null
        # 'http://2sc.cheshi.com/info/613087.html',  # control is null
        # 'http://2sc.cheshi.com/info/1142352.html',  # mile < 0.00
        # 'http://2sc.cheshi.com/info/626799.html',  # city like *地区
        # 'http://2sc.cheshi.com/info/1757057.html',  # volume is None
        # 'http://2sc.cheshi.com/info/1765834.html' # imgurls
        # 'http://2sc.cheshi.com/info/1766391.html',  # control is null
    ],

    'parse': parse_rule,
    # 'parse_list': parse_list,

    'parse_detail': {
        "item": item_rule,
    }
}

fmt_rule_urls(rule)
# rule['parse'] = rule['parse_detail']
