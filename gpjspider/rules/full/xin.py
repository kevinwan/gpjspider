# -*- coding: utf-8 -*-
"""
优信二手车 优质二手车 规则
"""
from gpjspider.utils.constants import SOURCE_TYPE_SELLER
from .utils import *

item_rule = {
    "class": "UsedCarItem",
    "fields": {
        'title': {
            'xpath': ('//div[@class="tit"]/h1/text()',),
            'required': True,
        },
        'meta': {
            'xpath': ('//meta[@name="description"]/@content',),
        },
        'year': {
            'xpath': (u'//li[@class="br"]/span[contains(text(), "上牌时间")]/../em/text()',),
        },
        'month': {
            'xpath': (u'//li[@class="br"]/span[contains(text(), "上牌时间")]/../em/text()',),
        },
        'mile': {
            'xpath': (u'//li[@class="br"]/span[contains(text(), "行驶里程")]/../em/text()',),
        },
        'volume': {
            'xpath': (u'//li[@class="br"]/span[contains(text(), "排量")]/../em/text()',),
        },
        'phone': {
            'xpath': (
                # '//span[@id="tel_num"]/@tel',
                text(with_cls('tel', '//span')),
            ),
            'after': ' ',
        },
        'color': {
            'xpath': (u'//td[contains(text(), "颜色")]/following-sibling::td/text()',),
        },
        'control': {
            'xpath': (u'//td[contains(text(), "变速箱")]/following-sibling::td/text()',),
        },
        'region': {
            'xpath': (
                '//div[@class="company"]/p[2]/text()',
            ),
        },
        'price': {
            'xpath': (u'//div[@class="wan_1"]/em/text()',),
        },
        'price_bn': {
            'xpath': (u'//div[@class="wan_2"]/span/del/text()',),
        },
        'brand_slug': {
            'xpath': ('//div[@class="tit"]/h1/text()',),
        },
        'model_slug': {
            'xpath': ('//div[@class="tit"]/h1/text()',),
        },
        'city': {
            'xpath': (u'//li/span[contains(text(), "销售城市")]/../em/text()',),
        },
        'description': {
            'xpath': (u'//div[@class="test-report"]/div[@class="test-txt"]/ul/li/text()',),
            'processors': ['join'],
        },
        'imgurls': {
            'xpath': ('//div[@class="carimg"]/div/img/@src',),
            'processors': ['join'],
        },
        'mandatory_insurance': {
            'xpath': (u'//td[contains(text(), "保险到期时间")]/following-sibling::td/text()',),
        },
        'company_name': {
            'xpath': ('//div[@class="newcompany"]/p/text()',),
        },
        'company_url': {
            'xpath': ('//div[@class="newcompany"]/a/@href',),
            'format': True,
        },
        'examine_insurance': {
            'xpath': (
                u'//td[contains(text(), "年检有效期")]/following-sibling::td/text()',
            ),
        },
        'transfer_owner': {
            'xpath': (
                after_has(u'过户次数'),
            ),
        },
        'car_application': {
            'xpath': (
                after_has(u'使用性质'),
            ),
        },
        'maintenance_desc': {
            'xpath': (
                after_has(u'保养情况'),
            ),
        },
        'quality_service': {
            'xpath': (
                img(cls('day-pic')),
            ),
            'default': u'',
            'processors': ['first', 'xin.quality_service']
        },
        'time': {
            'xpath': (
                after_has(u'检测时间', 'text()'),
            ),
        },
        'source_type': {
            'default': SOURCE_TYPE_SELLER,
        },
        'is_certifield_car': {
            'xpath': (
                img(cls('day-pic')),
            ),
            'default': False,
            'processors': ['xin.is_certifield_car']
        },
    },
}

parse_rule = {
    "url": {
        "xpath": (
            url(has_cls('car-box', '//p')),
        ),
        "format": "http://www.xin.com{0}",
        'contains': '/c/',
        "step": 'parse_detail',
    },
    "next_page_url": {
        "default": True
    },
}

rule = {
    # ==========================================================================
    # 基本配置
    # ==========================================================================
    'name': u'优信二手车',
    'domain': 'xin.com',
    'start_urls': [
        'http://www.xin.com/quanguo/s/o2a10i1v1/',
    ],
    'base_url': 'http://www.xin.com',
    'per_page': 20,
    'pages': 12000,

    #==========================================================================
    #  默认步骤  parse
    #==========================================================================
    'parse': parse_rule,
    #==========================================================================
    #  详情页步骤  parse_detail
    #==========================================================================
    'parse_detail': {
        "item": item_rule,
    }
}

fmt_rule_urls(rule)
