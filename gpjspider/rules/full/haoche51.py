# -*- coding: utf-8 -*-
from gpjspider.utils.constants import SOURCE_TYPE_SELLER
from .utils import *


def format_func(url_str):
    """
    javascript:window.open('http://bj.haoche51.com/details/20003.html')
    """
    s = url_str.find("javascript:window.open('")
    if s >= 0:
        s += len("javascript:window.open('")
    else:
        return None
    if not url_str.endswith("')"):
        return None
    else:
        return url_str[s:-2]


item_detail = {
    "class": "UsedCarItem",
    "fields": {
        'title': {
            'xpath': (
                text(cls("autotit", "/strong")),
                '//div[@class="autotit"]/strong/text()',
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
                text(cls("autotit", "/h2")),
                #'//div[@class="autotit"]/h2/text()',
            ),
        },
        'month': {
            'xpath': (
                text(cls("autotit", "/h2")),
                #'//div[@class="autotit"]/h2/text()',
            ),
        },
        'mile': {
            'xpath': (
                text(cls("autotit", "/h2")),
                #'//div[@class="autotit"]/h2/text()',
            ),
        },
        'volume': {
            'xpath': (
                after_has(u'排量', 'li[1]'),
                #u'//li[contains(text(), "排量")]/following-sibling::li[1]/text()',
            ),
        },
        'control': {
            'xpath': (
                text(cls("autotit", "/h2")),
                #'//div[@class="autotit"]/h2/text()',
            ),
            'processors': ['first', 'haoche51.control'],
        },
        'price': {
            'xpath': (
                text(cls("car-quotation", "/strong")),
                #'//div[@class="car-quotation"]/strong/text()',
            ),
        },
        'price_bn': {
            'xpath': (
                after_has(u'厂商指导价', 'li[1]'),
            ),
            'regex': u'(.*)万元?'
        },
        'brand_slug': {
            'xpath': (
                text(cls("autotit", '/strong')),
                #'//div[@class="autotit"]/strong/text()',
            ),
        },
        'model_slug': {
            'xpath': (
                text(cls("crumbs", "/a[4]")),
                text(cls("autotit", '/strong')),
                #'//div[@class="autotit"]/strong/text()',
            ),
            'regex': u'.*二手(.*)'
        },
        'city': {
            'xpath': (
                text(cls("crumbs", "/a[1]")),
                # '//div[@class="autotit"]/h2/text()',
            ),
            'regex': u'(.*?)好车无忧',
            # 'processors': ['first', 'haoche51.city'],
        },
        'region': {
            'xpath': (
                text(id_("kanche_addr")),
                # '//p[@class="own"]/text()',
            ),
            # 'processors': ['first', 'haoche51.region'],
        },
        'description': {
            'xpath': (
                text(cls("f-type03")),
                text(cls("ow-sa", "/p[not(@class)]")),
                #'//p[@class="f-type03"]/text()',
                #'//div[@class="ow-sa"]/p[not(@class)]/text()'
            ),
        },
        'imgurls': {
            'xpath': (
                '//ul[@class="mrd_ul"]/li/a/img/@data-original',
                '//div[@class="dt-pictype"]/img/@data-original',
            ),
            'processors': ['join', 'raw_imgurls'],
            'processors': ['join', 'strip_imgurls'],
        },
        'condition_detail': {
            'xpath': (
                "//div[@class='cd-pc']/text()[4]",
            ),
        },
        'contact': {
            'xpath': (
                '//p[@class="own"]/text()',
            ),
            'processors': ['first', 'haoche51.contact'],
        },
        'phone': {
            'xpath': (
                text(cls("tc-der", "/strong")),
                '//li[@class="tc-der"]/strong/text()',
            ),
        },
        'mandatory_insurance': {
            'xpath': (
                has(u"交强险有效期", prefix="/ul/li"),
                u'//div[@class="ow-sa1"]/ul/li[contains(text(), "交强")]/text()',
            ),
        },
        'business_insurance': {
            'xpath': (
                has(u"商业险有效期", prefix="/ul/li"),
                u'//div[@class="ow-sa1"]/ul/li[contains(text(), "商业")]/text()',
            ),
        },
        'examine_insurance': {
            'xpath': (
                has(u"年检有效期", prefix="/ul/li"),
                u'//div[@class="ow-sa1"]/ul/li[contains(text(), "年检")]/text()',
            ),
        },
        'transfer_owner': {
            'xpath': (
                text(cls('autotit', '/h2')),
                text(cls("ow-sa", "/div[contains(text(), '过户次数')]/strong")),
            ),
            'processors': ['first', 'haoche51.transfer_owner'],
            'default': 0,
        },
        'quality_service': {
            'xpath': (
                text(cls('wyno')),
            ),
        },
        'source_type': {
            'default': SOURCE_TYPE_SELLER,
        },
        'driving_license': {
            'xpath': (
                has(u"行驶证", prefix="//li"),
                #u'//li[contains(text(), "行驶证")]/text()',
            ),
            'processors': ['first', 'haoche51.driving_license'],
        },
        'invoice': {
            'xpath': (
                has(u"购车发票", prefix="//li"),
                #u'//li[contains(text(), "购车发票")]/text()',
            ),
            'processors': ['first', 'haoche51.invoice'],
        },
    },
}

parse_list_rule = {
    "url": {
        "xpath": (
            '//div[@class="content"]/div/div/@onclick',
        ),
        "format": format_func,
        "step": 'parse_detail',
        # 'update': True,
        # 'category': 'usedcar'
    },
    "next_page_url": {
        "xpath": (
            u'//a[contains(text(), "下一页")]/@href',
        ),
        "excluded": ("javascript:void()",),
        # "format": "http://haoche.ganji.com{0}",
        "step": 'parse_list',
        # 'max_pagenum': 50,
        # 'incr_pageno': 1,
    },
}

rule = {
    'name': u'好车无忧',
    'domain': 'haoche51.com',
    'start_urls': [
        'http://bj.haoche51.com/vehicle_list.html',
        # 'http://nj.haoche51.com/details/24703.html',
        # 'http://sh.haoche51.com/details/29401.html',
    ],

    'parse': {
        "url": {
            "xpath": (
                url(has_cls('city-cs')),
                # '//div[@id="layer_follow1"]/ul/li/div/a/@href',
            ),
            "step": 'parse_list',
        }
    },
    'parse_list': parse_list_rule,

    'parse_detail': {
        "item": item_detail
    },
}

#rule['parse'] = rule['parse_detail']
