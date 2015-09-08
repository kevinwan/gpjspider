# -*- coding: utf-8 -*-
from gpjspider.utils.constants import *
from .utils import *

_has = lambda x: has(x, '/..')

item_rule = {
    "class": "UsedCarItem",
    "fields": {
        'title': {
            'xpath': (
                text(cls('car-title', '/h1')),
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
                text(cls('breadcrumb', '/a[5]/span')),
            ),
        },
        'year': {
            'xpath': (
                before_has(u'上牌时间'),
            ),
            'regex': u'(\d{4})年',
            'regex_fail': None,
        },
        'month': {
            'xpath': (
                before_has(u'上牌时间'),
            ),
            'regex': u'(\d{1,2})月',
        },
        # 'time': {
        # 'xpath': (
        # text(cls('f10 pr-5')),
        # ),
        # },
        'mile': {
            'xpath': (
                before_has(u'行驶里程'),
            ),
        },
        'volume': {
            'xpath': (
                has(u'关键参数'),
            ),
            'regex': r'\d\.?\d?',
        },
        'color': {
            'xpath': (
                '//title/text()',
            ),
            'processors': ['first', '51auto.color'],
            'processors': ['first', 'ygche.color'],
        },
        'control': {
            'xpath': (
                has(u'关键参数'),
            ),
            'processors': ['first', '51auto.control'],
        },
        'price': {
            'xpath': (
                text(cls('price')),
            ),
        },
        'price_bn': {
            'xpath': (
                text(cls('new-price')),
            ),
            'processors': ['first', '51auto.price_bn'],
        },
        'brand_slug': {
            'xpath': (
                text(cls('breadcrumb', '/a[3]')),
            ),
            'regex': u'二手(.*)',
        },
        'model_slug': {
            'xpath': (
                text(cls('breadcrumb', '/a[4]')),
            ),
            'regex': u'二手(.*)',
        },
        'model_url': {
            'xpath': (
                href(cls('breadcrumb', '/a[4]')),
            ),
            'format': True,
        },
        'city': {
            'xpath': (
                '//meta[@name="location"]/@content',
            ),
            'regex': u'city=(.*);',
        },
        'region': {
            'xpath': (
                '//*[@class="section-contact"]/text()[2]',
            ),
            'regex': u'看车地点：(.*)',
        },
        'status': {
            'xpath': (
                text(cls('sold-out')),
                u'//div[@class="tishimain"]/span[2]/text()',
            ),
            'processors': ['first', '51auto.status'],
            'default': 'Y',
        },
        'phone': {
            'xpath': (
                '//input[@id="tels"]/@value',
                text(id_('contact-tel1', '/p')),
            ),
            'processors': ['first']
        },
        'contact': {
            'xpath': (
                '//*[@class="section-contact"]/text()[1]',
                '//' + has_cls('section-contact', '/p/text()[1]'),
            ),
            'regex': u'联系人：(.*)',
        },
        'company_name': {
            'xpath': (
                text(cls('car-market', '/h1/a')),
            ),
        },
        'company_url': {
            'xpath': (
                attr(cls('car-market', '/h1/a'), 'href'),
            ),
        },
        'driving_license': {
            'xpath': (
                has(u'行驶证'),
            ),
            'regex': u'行驶证：(.*)',
        },
        'invoice': {
            'xpath': (
                has(u'过户发票'),
            ),
            'regex': u'过户发票：(.*)',
        },
        # 'maintenance_record': {
        # 'xpath': (
        # _has(u'保养方式'),
        # ),
        # },
        'quality_service': {
            'xpath': (
                '//*[@class="section-safe"]/span//text()',
            ),
            'processors': ['join'],
        },
        'description': {
            'xpath': (
                text(cls('car-detail-container', '/p[2]')),
            ),
        },
        'imgurls': {
            'xpath': (
                attr(cls('lazy'), 'data-original'),
            ),
            'processors': ['51auto.imgurls'],
        },
        'mandatory_insurance': {
            'xpath': (
                has(u'交强险'),
            ),
            'regex': u'交强险截止日期：(.*)',
        },
        # 'business_insurance': {
        # 'xpath': (
        # _has(u'商业险'),
        # ),
        # },
        'examine_insurance': {
            'xpath': (
                has(u'车辆年审'),
            ),
            'regex': u'车辆年审日期：(.*)',
        },
        'transfer_owner': {
            'xpath': (
                has(u'过户次数'),
            ),
            'regex': u'过户次数：(.*)',
        },
        'is_certifield_car': {
            'default': False,
            'default': '%(quality_service)s',
            'default_fail': None,
        },
        'source_type': {  # 本网站含 品牌认证、商家认证、个人二手车
            'xpath': (
                '//title/text()',
            ),
            'processors': ['first', '51auto.source_type'],
        },
        'car_application': {
            'xpath': (
                has(u'车辆用途'),
            ),
            'regex': u'车辆用途：(.*)',
        },
        # 'condition_level': {
        #     'xpath':(
        #     ),
        # },
        'condition_detail': {
            'xpath': (
                has_attr2(u'准新车', 'title'),
            ),
        },
    },
}

parse_rule = {
    "url": {
        "re": (
            r'http://www\.51auto\.com/buycar/\d+\.html',
        ),
        "step": 'parse_detail',
    },
    "next_page_url": {
        "xpath": (
            next_page(),
        ),
        'format': True,
        'format': '{url}',
        'format': '%(url)s',
        # 'format': 'no',
        'regex': '(\d+)',
        'replace': ['(pageNo=\d+)', 'curentPage={0}'],
        "step": 'parse',
        # 'incr_pageno': 3,
    },
}


parse_list = {
    'url': {
        're': (
            r'http://www.51auto.com/buycar/\d+.html',
        ),
        'step': 'parse_detail',
    },
    'next_page_url': {
        'xpath': (
            next_page(),
        ),
        'excluded': ['javascript'],
        'format': '%(url)s',
        'regex': 'pageNo=(\d+)',
        'replace': ['(pageNo=\d+)', 'pageNo={0}'],
        'step': 'parse_list',
        # 'dont_filter': False,
    },
}


rule = {
    'name': u'51汽车',
    'domain': '51auto.com',
    'base_url': 'http://www.51auto.com',
    'dealer': {
        'url': 'http://www.51auto.com/control/VehiclesList?id=%s&pageNo=1',
        'regex': r'dealers/(\d+)'
    },
    'start_urls': [
        # 'http://www.51auto.com/quanguo/pabmdcigf?searchtype=searcarlist&orderValue=record_time&status=3&isPicture=1&curentPage=1&isgotopage=1',
        'http://www.51auto.com/quanguo/pabmdcigf?searchtype=searcarlist&orderValue=record_time&curentPage=1&isgotopage=1',
        'http://www.51auto.com/quanguo/pabmdcig1f?searchtype=searcarlist&orderValue=record_time&curentPage=1&isgotopage=1',
        'http://www.51auto.com/quanguo/pabmdcig2f?searchtype=searcarlist&orderValue=record_time&curentPage=1&isgotopage=1',
        'http://www.51auto.com/quanguo/pabmdcig0f?searchtype=searcarlist&orderValue=record_time&curentPage=1&isgotopage=1',
        # 'http://www.51auto.com/quanguo/search/?img=y&onsale=y&ordering=publishTime&direction=2&page=10',
        # 'http://hx2car.com/car/search.htm?carFlag=essence&more=f0010000ytdzsejckbmgl100000',
        # 'http://www.51auto.com/buycar/2618559.html',
        # 'http://www.51auto.com/buycar/2622130.html', # 准新车，有商家检测
        # 'http://www.51auto.com/buycar/2645362.html', # 无相关检测
        # 'http://www.51auto.com/buycar/2641587.html', # 商家、过户次数未知、无检测
        # 'http://www.51auto.com/buycar/2646783.html', # 个人车源
        # 'http://www.51auto.com/buycar/2646898.html', # 商家车源
        # 'http://www.51auto.com/buycar/2482736.html', # 品牌车商
        # 'http://www.51auto.com/buycar/2623865.html',  # -model_slug（进口）
        # 'http://www.51auto.com/buycar/2873991.html' # phone=1390784****
    ],
    'per_page': 24,
    'pages': 3000,

    'parse': parse_rule,
    'parse_list': parse_list,
    'parse_detail': {
        "item": item_rule,
    }
}

fmt_rule_urls(rule)
# rule['parse'] = rule['parse_detail']
