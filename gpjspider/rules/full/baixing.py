# -*- coding: utf-8 -*-
from .utils import *

item_rule = {
    "class": "UsedCarItem",
    "fields": {
        'title': {
            'xpath': (
                text(has_cls("viewad-title")),
            ),
            'required': True,
        },
        'dmodel': {
            'xpath': (
                has(u'车型：'),
            ),
        },
        'meta': {
            'xpath': ('//meta[@name="description"]/@content',),
        },
        'year': {
            'xpath': (
                has(u'上牌年份：'),
            ),
        },
        'month': {
            'xpath': (
                has(u'上牌年份：'),
            ),
        },
        'mile': {
            'xpath': (
                has(u'行驶里程：'),
            ),
        },
        'volume': {
            'default': '%(dmodel)s',
        },
        'phone': {
            'xpath': (
                text(with_cls('tel', '//span')),
            ),
            'after': ' ',
        },
        'color': {
            'xpath': (
                has(u'车辆颜色：'),
            ),
            'regex': u'：(.*)',
        },
        'control': {
            'xpath': (
                has(u'变速箱：'),
            ),
            'default': '%(dmodel)s',
            'regex': u' ([手自]\S*[动体])',
            'regex_fail': None,
        },
        'region': {
            'xpath': (
                has(u'地区：', '/a/text()'),
            ),
            'processors': ['join']
        },
        'price': {
            'xpath': (
                has(u'价格：'),
            ),
        },
        'price_bn': {
            'xpath': (

            ),
        },
        'brand_slug': {
            'xpath': (
                has(u'品牌：', '/a'),
            ),
        },
        'model_slug': {
            'xpath': (
                has(u'车系列：'),
            ),
        },
        'city': {
            'xpath': (
                '//meta[@name="location"]/@content',
            ),
            'regex': 'city=(.*)',
        },
        'description': {
            'xpath': (
                '//meta[@name="description"]/@content',
            ),
        },
        'imgurls': {
            'xpath': (
                u'//div[@class="img sep"]/div/img/@src',
            ),
            'processors': ['join'],
        },
        'mandatory_insurance': {
            'xpath': (
                has(u'交强险到期：'),
            ),
        },
        'company_name': {
            'xpath': (
                text(cls("shop-topic", '/a')),
            ),
        },
        'company_url': {
            'xpath': (
                url(cls("shop-topic")),
            ),
        },
        'examine_insurance': {
            'xpath': (
                has(u'年检到期：'),
            ),
        },
        # 'transfer_owner': {
        #     'xpath': (
        #         after_has(u'过户次数'),
        #     ),
        # },
        'car_application': {
            'xpath': (
                has(u'车辆用途：'),
            ),
        },
        # 'maintenance_desc': {
        #     'xpath': (
        #
        #     ),
        # },
        # 'quality_service': {
        #     'xpath': (
        #
        #     ),
        # },
        'time': {
            'xpath': (
                u'//span[contains(@title, "首次发布于")]/@title',
            ),
            'regex': u'：(.*)',
        },
        # 'is_certifield_car': {
        #     'xpath': (),
        # },
        'source_type': {
            'default': "%(company_name)s",
            'processors': ['baixing.source_type']
        },
    },
}

parse_rule = {
    "url": {
        "xpath": (
            '//li[@data-aid]/a/@href',
        ),
        'contains': '/ershouqiche/',
        "step": 'parse_detail',
    },
    "next_page_url": {
        "xpath": (
            u'//a[contains(text(), "下一页")]/@href',
        ),
        "format": 'http://china.baixing.com{0}',
        "step": 'parse',
    },
}

rule = {
    'name': u'百姓二手车',
    'domain': 'baixin.com',
    'start_urls': [
        'http://china.baixing.com/ershouqiche/?imageFlag=1',
        # 'http://shanghai.baixing.com/ershouqiche/a749685037.html',
        # 'http://nanning.baixing.com/ershouqiche/a751473084.html',
        # 'http://dalian.baixing.com/ershouqiche/a761320262.html',
    ],
    # 'base_url': 'http://china.baixin.com',
    # 'per_page': 20,
    # 'pages': 100,

    'parse': parse_rule,

    'parse_detail': {
        "item": item_rule,
    }
}

fmt_rule_urls(rule)
#rule['parse'] = rule['parse_detail']
