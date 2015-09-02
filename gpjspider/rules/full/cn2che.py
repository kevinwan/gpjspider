# -*- coding: utf-8 -*-
"""
273二手车
"""
from gpjspider.utils.constants import *
from .utils import *

_has = lambda x: has(x, '/..')

item_rule = {
    "class": "UsedCarItem",
    "fields": {
        'title': {
            'xpath': (
                text(id_('title')),
            ),
            'required': True,
        },
        'meta': {
            'xpath': (
                '//meta[@name="description" or @name="Description"]/@content',
            ),
        },
        'dmodel': {
            #'xpath': (
                #after_has(u'本车标签'),
            #),
            'default': '%(title)s',
            'processors': ['cn2che.dmodel'],
        },
        'year': {
            'xpath': (
                has(u'上牌时间'),
            ),
        },
        'month': {
            'xpath': (
                has(u'上牌时间'),
            ),
        },
        'time': {
            'xpath': (
                has(u'更新时间'),
            ),
            'regex': u'更新时间：(.*)',
        },
        'mile': {
            'xpath': (
                has(u'行驶里程'),
            ),
            'regex': u'行驶里程：(.*)',
        },
        'volume': {
            'xpath': (
                after_has(u'排量', 'td[@class="table02" and not(contains(text(), "-")) and re:match(text(), "\d")]'),
            ),
            'default': '%(title)s',
            'processors': ['first', 'cn2che.volume'],
        },
        'color': {
            'xpath': (
                after_has(u'汽车颜色'),
            ),
            'regex': u'(.*色)',
            'regex_fail': None,
        },
        'control': {
            'xpath': (
                after_has(u'变 速 器'),
            ),
            'regex': u'([手自]{1,2}一?[动体])',
            'regex_fail': None,
        },
        'price': {
            'xpath': (
                has(u'二手车价格', '/strong'),
            ),
        },
        #'price_bn': {
            #'xpath': (
                #has(u'出厂报价', '/strong[1]'),
            #),
            #'regex': '(\d+\.?\d*)',
        #},
        'brand_slug': {
            'xpath': (
                has(u'车辆品牌'),
            ),
            'regex': u'车辆品牌：(.*)',
        },
        'model_slug': {
            'xpath': (
                has(u'车辆系列'),
            ),
            'regex': u'车辆系列：(.*)',
        },
        'model_url': {
            'xpath': (
                href(cls('sell_nav', '/a[4]')),
            ),
            'format': True,
        },
        'status': {
            'xpath': (
                has(u'车辆类型'),
            ),
            'processors': ['first', 'cn2che.status'],
        },
        'city': {
            'xpath': (
                attr(id_('jydq'), 'title'),
            ),
        },
        'region': {
            'xpath': (
                after_has(u'联系地址'),
            ),
        },
        'phone': {
            'xpath': (
                text(id_('phone')),
            ),
        },
        'contact': {
            'xpath': (
                text(id_('linkman')),
            ),
        },
        'company_name': {
            'xpath': (
                text(id_('shopname1', '/a')),
            ),
        },
        'company_url': {
            'xpath': (
                href(id_('shopname1', '/a')),
            ),
        },
        #'driving_license': {
            #'xpath': (
                #'//*[@id="other_infor1"]/div[1]/p/span[2]/text()',
            #),
        #},
        #'invoice': {
            #'xpath': (
                #'//*[@id="other_infor1"]/div[1]/p/span[4]/text()',
            #),
        #},
        #'maintenance_record': {
            #'xpath': (
                #has(u'保养情况', '/..'),
            #),
        #},
        #'quality_service': {
            #'xpath': (
                #attr(cls('ensure', '/a'), 'title'),
            #),
            #'processors': ['join'],
        #},
        'description': {
            'xpath': (
                text(cls('describe')),
            ),
        },
        'imgurls': {
            'xpath': (
                '//*[@class="contentdiv"]//img/@src',
            ),
            'processors': ['join'],
        },
        'mandatory_insurance': {
            'xpath': (
                after_has(u'保 险'),
            ),
        },
        #'business_insurance': {
            #'xpath': (
                #_has(u'商业险'),
            #),
        #},
        'examine_insurance': {
            'xpath': (
                after_has(u'年 检'),
            ),
        },
        #'transfer_owner': {
            #'xpath': (
                #has(u'过户次数'),
            #),
            #'regex': u'过户次数：(.*)',
        #},
        'is_certifield_car': {
            'default': 0,
        },
        'source_type': {
            'xpath': (
                has(u'车商信息'),
                has(u'会员信息'),
            ),
            'processors': ['first', 'cn2che.source_type'],
        },
        'car_application': {
            'xpath': (
                after_has(u'原车用途'),
            ),
            'regex': u'(.*运)',
            'regex_fail': None,
        },
        #'condition_level': { # 原网站有 车况 的字段，但是都是 非常好，没什么用
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
    'url': {
        're': (
            r'http://www\.cn2che\.com/sellcarinfo_\d+\.html',
        ),
        #'format': True,
        'step': 'parse_detail',
    },
    'next_page_url': {
        "xpath": (
            href(cls('cheyuan', '/ol/li/a')),
            next_page(),
        ),
        'format': True,
        'step': 'parse',
        # 'incr_pageno': 3,
    },
}


rule = {
    'name': u'中国二手车城',
    'domain': 'cn2che.com',
    'base_url': 'http://www.cn2che.com',
    'start_urls': [
        'http://www.cn2che.com/buycar/cccpcmp1bcrmplos2/',
        'http://www.cn2che.com/buycar/cccpcmp1bcrmp1lo3s2/', # 全国、最新发布倒序、只看有图
        #'http://www.cn2che.com/sellcarinfo_1872380.html', # 排量 6.7L、已删除
        #'http://www.cn2che.com/sellcarinfo_1921877.html', # 排量 2996mL、在售、年检
        #'http://www.cn2che.com/sellcarinfo_1921892.html', # 年检、保险
        #'http://www.cn2che.com/sellcarinfo_1921892.html', # 个人车源
        #'http://www.cn2che.com/sellcarinfo_1838726.html', # 营运车辆
        #'http://www.cn2che.com/sellcarinfo_1921509.html', # 排量 9.725L
        # 'http://www.cn2che.com/sellcarinfo_1931169.html',
    ],

    'parse': parse_rule,

    'parse_detail': {
        "item": item_rule,
    }
}

fmt_rule_urls(rule)
# rule['parse'] = rule['parse_detail']
