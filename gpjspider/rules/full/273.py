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
                text(id_('detail_main_info', '/h1/b')),
            ),
            'required': True,
        },
        'meta': {
            'xpath': (
                '//meta[@name="description" or @name="Description"]/@content',
            ),
        },
        'dmodel': {
            'xpath': (
                after_has(u'本车标签'),
            ),
            'processors': ['273.dmodel'],
        },
        'year': {
            'xpath': (
                has(u'上牌时间', '/strong'),
            ),
            'regex': u'(\d{4})年',
            'regex_fail': None,
        },
        'month': {
            'xpath': (
                has(u'上牌时间', '/strong'),
            ),
            'regex': u'(\d{1,2})月',
            'regex_fail': None,
        },
        'time': {
            'xpath': (
                has(u'发布时间', '/..'),
            ),
        },
        'mile': {
            'xpath': (
                has(u'表显里程', '/strong'),
            ),
        },
        'volume': {
            'xpath': (
                has(u'排量', '/..').replace('*[', '*[not(contains(text(), "0.00L"))]/*['),
            ),
            'default': '%(title)s',
        },
        'color': {
            'xpath': (
                has(u'车身颜色', '/..'),
            ),
        },
        'control': {
            'xpath': (
                has(u'变速箱', '/..'),
            ),
        },
        'price': {
            'xpath': (
                has(u'车主报价', '/strong'),
            ),
        },
        'price_bn': {
            'xpath': (
                has(u'出厂报价', '/strong[1]'),
            ),
            'regex': '(\d+\.?\d*)',
        },
        'brand_slug': {
            'xpath': (
                text(id_('bread', '/div[1]/a[4]')),
            ),
            'regex': u'二手(.*)',
        },
        'model_slug': {
            'xpath': (
                text(id_('bread', '/div[1]/a[5]')),
            ),
            'regex': u'二手(.*)',
        },
        'model_url': {
            'xpath': (
                href(id_('bread', '/div[1]/a[5]')),
            ),
            'format': True,
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
                text(id_('bread', '/div[1]/a[1]')),
            ),
            'regex': u'(.*?)二手',
        },
        'region': {
            'xpath': (
                u'//*[contains(text(), "终点")]/following-sibling::*/@value',
            ),
        },
        'status': {
            'xpath': (
                u'//div[@class="tips_shelf"]/strong[contains(text(),"非常抱歉，该车辆已下架")]',
                u'//div[@id="page404"]/div[@class="tishi" and contains(text(), "后页面自动跳转")]',
            ),
            'default': 'Y',
        },
        'phone': {
            'xpath': (
                after_has(u'电话', 'strong'),
            ),
            'processors': ['join'],
        },
        'contact': {
            'xpath': (
                '//*[@id="trans_ad"]//*[@class="name"]/a/text()',
            ),
        },
        'company_name': {
            'xpath': (
                after_has(u'门店', 'a'),
            ),
        },
        'company_url': {
            'xpath': (
                u'//*[contains(text(), "门店")]/following-sibling::a/@href',
            ),
        },
        'driving_license': {
            'xpath': (
                '//*[@id="other_infor1"]/div[1]/p/span[2]/text()',
            ),
        },
        #'invoice': {
            #'xpath': (
                #'//*[@id="other_infor1"]/div[1]/p/span[4]/text()',
            #),
        #},
        'maintenance_record': {
            'xpath': (
                has(u'保养情况', '/..'),
            ),
        },
        'quality_service': {
            'xpath': (
                attr(cls('ensure', '/a'), 'title'),
            ),
            'processors': ['join'],
        },
        'description': {
            'xpath': (
                text(cls('sub_content', '/p')),
            ),
        },
        'imgurls': {
            'xpath': (
                attr(cls('car_photo', '/ul/li/img'), 'data-url'),
            ),
            'processors': ['join'],
        },
        'mandatory_insurance': {
            'xpath': (
                has(u'交强险', '/..'),
            ),
        },
        #'business_insurance': {
            #'xpath': (
                #_has(u'商业险'),
            #),
        #},
        'examine_insurance': {
            'xpath': (
                has(u'年检情况', '/..'),
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
            'default': SOURCE_TYPE_ODEALER,
        },
        'car_application': {
            'xpath': (
                has(u'使用性质', '/..'),
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
    "url": {
        're': (
            r'http://\w+\.273\.cn/car/\d+\.html',
        ),
        #'format': True,
        "step": 'parse_detail',
        'update': True,
        'category': 'usedcar'
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
            r'http://\w+\.273\.cn/car/\d+\.html',
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
    'name': u'273二手车',
    'domain': '273.cn',
    'base_url': 'http://www.273.cn',
    'dealer': {
        'url': '%s/os1_otd/',
    },
    'start_urls': [
        # 'http://www.273.cn/os1_otd/?page=119',
        'http://www.273.cn/os1_otd/', # 全国、时间倒序
        #'http://fz.273.cn/car/15986010.html', # 门店验车、车况检测
        #'http://yx.273.cn/car/16094479.html', # 行驶证已审核
        #'http://lps.273.cn/car/16094464.html', # 普通车源
        # 'http://xm.273.cn/car/16464549.html',  # volume is 0.00
        # 'http://km.273.cn/car/16019892.html',  # mile is None
        # 'http://km.273.cn/car/16586850.html',  # dmodel list cant replace
    ],
    'per_page': 20,
    'pages': 300,

    'parse': parse_rule,
    'parse_list': parse_list,
    'parse_detail': {
        "item": item_rule,
    }
}

fmt_rule_urls(rule)
# rule['parse'] = rule['parse_detail']
