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
            'xpath': (
                text(has_cls("tit", "/h1")),
            ),
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
            'xpath': (
                u'//div[@class="info"]/ul/li[2]/em//text()',
                u'//li[@class="br"]/span[contains(text(), "行驶里程")]/../em/text()',
            ),
        },
        'volume': {
            'xpath': (u'//li[@class="br"]/span[contains(text(), "排量")]/../em/text()',),
            'default': '%(title)s',
        },
        'phone': {
            'xpath': (
                text(with_cls('tel', '//span')),
            ),
            'after': ' ',
        },
        'color': {
            'xpath': (u'//td[contains(text(), "颜色")]/following-sibling::td/text()',),
        },
        'control': {
            'xpath': (u'//td[contains(text(), "变速箱")]/following-sibling::td/text()',),
            'default': '%(title)s',
        },
        'region': {
            'xpath': (
                text(cls("company", "/p[2]")),
            ),
        },
        'price': {
            'xpath': (
                text(cls("wan_1", "/em")),
            ),
        },
        'price_bn': {
            'xpath': (
                text(cls("wan_2", "/span/del")),
            ),
        },
        'brand_slug': {
            'xpath': (
                text(cls("tit", '/h1')),
            ),
        },
        'model_slug': {
            'xpath': (
                text(cls("tit", '/h1')),
            ),
        },
        'city': {
            'xpath': (
                has(u'销售城市', '/../em', 'li/span'),
                u'//li/span[contains(text(), "销售城市")]/../em/text()',
            ),
        },
        'description': {
            'xpath': (
                u'//div[@class="test-report"]/div[@class="test-txt"]/ul/li/text()',
            ),
            'processors': ['join'],
        },
        'imgurls': {
            'xpath': (
                img(cls("carimg", "/div/img")),
                '//div[@class="carimg"]/div/img/@src',
            ),
            'processors': ['join'],
        },
        'mandatory_insurance': {
            'xpath': (
                after_has(u'保险到期', 'td', 'td'),
                u'//td[contains(text(), "保险到期时间")]/following-sibling::td/text()',
            ),
        },
        'company_name': {
            'xpath': (
                text(cls("newcompany", "/p")),
                '//div[@class="newcompany"]/p/text()',
            ),
        },
        'company_url': {
            'xpath': (
                url(cls("newcompany", "/a")),
                '//div[@class="newcompany"]/a/@href',
            ),
            'format': True,
        },
        'examine_insurance': {
            'xpath': (
                after_has(u'年检有效期'),
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
        # 'quality_service': {
        # 'xpath': (
        #         img(cls('day-pic')),
        #     ),
        #     'default': u'',
        #     'processors': ['first', 'xin.quality_service']
        # },
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
                exists(img(cls('day-pic'))),
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
        "xpath": (
            u'//a[contains(text(), "下一页")]/@data-page',
        ),
        "format": 'http://www.xin.com/quanguo/s/o2a10i{0}v1/',
        "step": 'parse',
    },
}

rule = {
    'name': u'优信二手车',
    'domain': 'xin.com',
    'start_urls': [
        'http://www.xin.com/quanguo/s/o2a10i1v1/',
    ],
    'base_url': 'http://www.xin.com',
    'per_page': 20,
    'pages': 12000,

    'parse': parse_rule,

    'parse_detail': {
        "item": item_rule,
    }
}

fmt_rule_urls(rule)
