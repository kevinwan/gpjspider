# -*- coding: utf-8 -*-
"""
爱卡二手车
"""
from gpjspider.utils.constants import *
from .utils import *

_has = lambda x: has(x, '/..')

item_rule = {
    "class": "UsedCarItem",
    "fields": {
        'title': {
            'xpath': (
                text(cls('specifics_title', '/h1')),
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
                #text(cls('breadcrumb', '/a[5]/span')),
            #),
            'default': '%(title)s',
        },
        'year': {
            'xpath': (
                has(u'首次上牌', '/..'),
            ),
            'regex': u'(\d{4})年',
            'regex_fail': None,
        },
        'month': {
            'xpath': (
                has(u'首次上牌', '/..'),
            ),
            'regex': u'(\d{1,2})月',
        },
        'time': {
            'xpath': (
                has(u'发布时间'),
            ),
            'regex': u'发布时间：(.*)',
        },
        'mile': {
            'xpath': (
                after_has(u'行驶里程'),
            ),
        },
        'volume': {
            'xpath': (
                has(u'排　　量', '/..', 'li[not(contains(text(), "-")) and re:match(text(), "\d")]/span'),
            ),
            'default': '%(title)s',
            'processors': ['first', 'xcar.volume'],
        },
        'color': {
            'xpath': (
                has(u'车身颜色', '/..'),
            ),
        },
        'control': {
            'xpath': (
                after_has(u'变速箱'),
            ),
        },
        'price': {
            'xpath': (
                has(u'价格', '/span[contains(@class,"cost")]'),
            ),
        },
        'price_bn': {
            'xpath': (
                has(u'新车售价'),
            ),
            'regex': u'(\d+\.?\d*)',
        },
        'brand_slug': {
            'xpath': (
                text(cls('bread', '/a[3]')),
            ),
            'regex': u'二手(.*)',
        },
        'model_slug': {
            'xpath': [
                text(cls('bread', '/a[3]')),
                text(cls('bread', '/a[4]')),
            ],
            'processors': ['xcar.model_slug'],
        },
        'model_url': {
            'xpath': (
                href(cls('bread', '/a[4]')),
            ),
            'format': True,
        },
        'status': {
            'xpath': (
                '//i[@class="expired"]',
                # attr(cls('details_one', '/strong/img'), 'src'),
            ),
            'default': 'Y',
        },
        'city': {
            'xpath': (
                after_has(u'车辆地点'),
            ),
            'regex': u'.*?-(.*)',
        },
        'region': {
            'xpath': (
                has(u'看车地点', '/span'),
            ),
        },
        'phone': {
            'xpath': (
                after_has(u'联系电话'),
                attr(cls('details_one', '/strong/img'), 'src'),
            ),
            'format': True,
        },
        'contact': {
            'xpath': (
                text(cls('details_one', '/span')),
            ),
        },
        'company_name': {
            'xpath': (
                text(cls('shop_cont', '/h3')),
            ),
        },
        'company_url': {
            'xpath': (
                has_attr2(u'商家店铺', 'href'),
            ),
            'format': True,
        },
        #'driving_license': {
            #'xpath': (
                #has(u'行驶证'),
            #),
            #'regex': u'行驶证：(.*)',
        #},
        #'invoice': {
            #'xpath': (
                #has(u'过户发票'),
            #),
            #'regex': u'过户发票：(.*)',
        #},
        #'maintenance_record': {
            #'xpath': (
                #_has(u'保养方式'),
            #),
        #},
        #'quality_service': {
            #'xpath': (
               #'//*[@class="section-safe"]/span//text()',
            #),
            #'processors': ['join'],
        #},
        'description': {
            'xpath': (
                after_has(u'卖家附言'),
            ),
        },
        'imgurls': {
            'xpath': (
                '//*[@class="details_list2 clearfix mt12"]//img/@src',
            ),
            'processors': ['join'],
        },
        'mandatory_insurance': {
            'xpath': (
                after_has(u'保险有效日期'),
            ),
        },
        #'business_insurance': {
            #'xpath': (
                #_has(u'商业险'),
            #),
        #},
        'examine_insurance': {
            'xpath': (
                after_has(u'年检有效日期'),
            ),
        },
        #'transfer_owner': {
            #'xpath': (
                #has(u'过户次数'),
            #),
            #'regex': u'过户次数：(.*)',
        #},
        'is_certifield_car': {
            'xpath': (
                has(u'认证车'),
            ),
            'default': 0,
        },
        'source_type': {
            'xpath': (
                text(cls('shop_cont', '/h3')),
            ),
            'processors': ['first', 'xcar.source_type'],
            'default': SOURCE_TYPE_GONGPINGJIA,
        },
        'car_application': {
            'xpath': (
                after_has(u'车辆用途'),
            ),
        },
        #'condition_level': {
            #'xpath':(
            #),
        #},
        'condition_detail': {
            'xpath': (
                has(u'准新车'),
            ),
        },
    },
}

parse_rule = {
    "url": {
        "re": (
            r'/shop/\d+.htm',
        ),
        'format': True,
        "step": 'parse_detail',
    },
    "next_page_url": {
        "xpath": (
            next_page(),
        ),
        'format': True,
        "step": 'parse',
        # 'incr_pageno': 3,
    },
}


parse_list = {
    'url': {
        're': (
            r'/shop/\d+.htm',
        ),
        'format': True,
        'step': 'parse_detail',
    },
    'next_page_url': {
        'xpath': (
            next_page(),
        ),
        'excluded': ['javascript'],
        'format': True,
        'step': 'parse_list',
        # 'dont_filter': False,
    },
}


rule = {
    'name': u'爱卡汽车',
    'domain': 'used.xcar.com.cn',
    'base_url': 'http://used.xcar.com.cn',
    'dealer': {
        'url': '%s',
    },
    'start_urls': [
        # 'http://used.xcar.com.cn/search/0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0?sort=f5time&page=2',
        'http://used.xcar.com.cn/search/0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0?sort=f5time',
        'http://used.xcar.com.cn/search/0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-1-0/?sort=f5time',
        'http://used.xcar.com.cn/search/0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-2-0/?sort=f5time',
        'http://used.xcar.com.cn/search/0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-3-0/?sort=f5time',
        # 'http://used.xcar.com.cn/search/0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0?sort=f5time&page=2', # 只能从第二页开始，第一页网站报 500 错误
        #'http://used.xcar.com.cn/personal/2652840.htm', # 个人
        #'http://used.xcar.com.cn/shop/2540895.htm', # 商家、已售
        #'http://used.xcar.com.cn/shop/1099304.htm', # 认证车
        #'http://used.xcar.com.cn/shop/2604510.htm', # 准新车
        #'http://used.xcar.com.cn/shop/2604550.htm', # 报价太低警告
        # 'http://used.xcar.com.cn/shop/3183226.htm' # volume='2L'
        # 'http://used.xcar.com.cn/shop/3186290.htm' # volume='-''
        # 'http://used.xcar.com.cn/shop/3227189.htm' # price
        # 'http://used.xcar.com.cn/shop/3237295.htm',  # model_slug is 'V'
        # 'http://used.xcar.com.cn/shop/3270030.htm' # 联系电话
    ],

    'parse': parse_rule,
    'parse_list': parse_list,
    'parse_detail': {
        "item": item_rule,
    }
}

fmt_rule_urls(rule)
# rule['parse'] = rule['parse_detail']
