# -*- coding: utf-8 -*-
# from gpjspider.utils.constants import SOURCE_TYPE_SELLER
from .utils import *

item_rule = {
    "class": "UsedCarItem",
    "fields": {
        'title': {
            'xpath': (
                text(cls('dt-titletype')),
            ),
            'required': True,
        },
        'dmodel': {
            'default': '%(title)s',
        },
        'meta': {
            'xpath': (
                '//meta[@name="description" or @name="Description"]/@content',
            ),
        },
        'year': {
            'xpath': (
                text(cls('one', '/b')),
            ),
        },
        'month': {
            'xpath': (
                text(cls('one', '/b')),
            ),
        },
        'mile': {
            'xpath': (
                has(u'里程', '/b'),
            ),
        },
        'volume': {
            'xpath': (
                has(u'排量', '/b'),
            ),
            'default': '%(title)s',
        },
        'control': {
            'xpath': (
                has(u'变速箱', '/b'),
            ),
        },
        'price': {
            'xpath': (
                text(cls('f30 numtype')),
            ),
        },
        #  加上 price之后才是新车价
        'price_bn': {
            'xpath': (
                '//div[@class="pricebox"]/span[@class="f14"]/text()',
                # '//div[@class="pricebox"]/span[@class="f14"]/i/text()',
            ),
            'processors': ['first', 'ganjihaoche.price_bn'],
            'processors': ['concat'],
        },
        'phone': {
            'xpath': (
                text(cls('teltype')),
            ),
        },
        'brand_slug': {
            'xpath': (
                has(u'检测车型'),
            ),
            'processors': ['first', 'ganjihaoche.brand_slug'],
            'processors': ['first', 'after_colon'],
        },
        'model_slug': {
            'xpath': (
                has(u'检测车型'),
            ),
            'processors': ['first', 'ganjihaoche.model_slug'],
            'processors': ['first', 'after_colon', 'ganjihaoche.model_slug'],
        },
        'city': {
            'xpath': (
                text(cls('choose-city', '/span')),
            ),
        },
        'contact': {  # 联系人
            'xpath': (
                after_has(u'车主', 'text()'),
            ),
        },
        'region': {
            'xpath': (
                text(id_('base', '/ul/li[1]')),
            ),
            'processors': ['last']
        },
        'description': {
            'xpath': (
                text(cls('f-type03')),
            ),
        },
        'imgurls': {
            'xpath': (
                attr(cls('dt-pictype', '/img'), 'data-original'),
            ),
            'processors': ['join'],
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
                text(cls('baoxian')),
            ),
        },
        'examine_insurance': {
            'xpath': (
                text(cls('nianjian')),
            ),
        },
        'transfer_owner': {
            'xpath': (
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
            # 'default': SOURCE_TYPE_SELLER,
            'default': SOURCE_TYPE_GONGPINGJIA,
        },
    },
}

parse_rule = {
    "url": {
        "xpath": (
            url(has_cls('list-infoBox')),
        ),
        "format": True,
        "step": 'parse_detail',
    },
    "next_page_url": {
        "xpath": (
            '//a[@class="next"]/@href',
        ),
        "format": True,
        "step": 'parse',
        # 'incr_pageno': 10,
    },
}

rule = {
    'name': u'赶集好车',
    'domain': 'haoche.ganji.com',
    'base_url': 'http://haoche.ganji.com',
    'per_page': 20,
    'pages': 600,
    # 'update': True,
    'start_urls': [
        'http://haoche.ganji.com/www/buy/',
        # 'http://haoche.ganji.com/cn/buy/o2/',
        # 'http://haoche.ganji.com/cc/1713365366x.htm',
        # 'http://haoche.ganji.com/nj/1512163128x.htm',
        # 'http://haoche.ganji.com/bj/1514507784x.htm',
        # 'http://haoche.ganji.com/wh/1802111972x.htm',  # -model_slug 逍客-
        # 'http://haoche.ganji.com/bj/1802168768x.htm',  # -model_slug, 夏利A+-两厢-
        # 'http://haoche.ganji.com/cs/1792525820x.htm',  # -model_slug 1.6L
        # 'http://haoche.ganji.com/cd/1533562332x.htm',  # -model_slug Cabrio-2012款
        # 'http://haoche.ganji.com/hf/1792116461x.htm',  # -model_slug Cross
        # 'http://haoche.ganji.com/qd/1792244639x.htm',  # -model_slug 1.2
        # 'http://haoche.ganji.com/bj/1792974854x.htm',  # -model_slug none
        # 'http://haoche.ganji.com/xa/1655751850x.htm',  # -model_slug 1.8L自动豪华
        # 'http://haoche.ganji.com/jn/1524333078x.htm',  # -model_slug 2007款
        # 'http://haoche.ganji.com/hz/1524440775x.htm',  # -model_slug 2.8T柴油多功能型短轴中顶
        # 'http://haoche.ganji.com/nj/1525397832x.htm',  # -model_slug 穿梭汽油标准版HFC4GA3
    ],

    'parse': parse_rule,

    'parse_detail': {
        "item": item_rule,
    },
}

fmt_rule_urls(rule)
# rule['parse'] = rule['parse_detail']
