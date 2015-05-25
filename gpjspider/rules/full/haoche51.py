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


rule = {
    #==========================================================================
    #  基本配置
    #==========================================================================
    'name': u'好车无忧',
    'domain': 'haoche51.com',
    'start_urls': [
        'http://bj.haoche51.com/vehicle_list.html',
        #  'http://nj.haoche51.com/details/24703.html',
    ],

    #==========================================================================
    #  默认步骤  parse
    #==========================================================================
    'parse': {
        "url": {
            "xpath": (
                url(has_cls('city-cs')),
                # '//div[@id="layer_follow1"]/ul/li/div/a/@href',
            ),
            "step": 'parse_list',
        }
    },
    #==========================================================================
    #  详情页步骤  parse_list
    #==========================================================================
    'parse_list': {
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
    },

    #==========================================================================
    #  详情页步骤  parse_detail
    #==========================================================================
    'parse_detail': {
        "item": {
            "class": "UsedCarItem",
            "fields": {
                'title': {
                    'xpath': ('//div[@class="autotit"]/strong/text()',),
                    'required': True,
                },
                'meta': {
                    'xpath': (
                        '//meta[@name="Description"]/@content',
                        '//meta[@name="description"]/@content'
                    ),
                },
                'year': {
                    'xpath': ('//div[@class="autotit"]/h2/text()',),
                },
                'month': {
                    'xpath': ('//div[@class="autotit"]/h2/text()',),
                },
                'mile': {
                    'xpath': ('//div[@class="autotit"]/h2/text()',),
                },
                'volume': {
                    'xpath': (
                        u'//li[contains(text(), "排量")]/following-sibling::li[1]/text()',
                    ),
                },
                'control': {
                    'xpath': ('//div[@class="autotit"]/h2/text()',),
                    'processors': ['first', 'haoche51.control'],
                },
                'price': {
                    'xpath': ('//div[@class="car-quotation"]/strong/text()',),
                },
                'price_bn': {
                    'xpath': ('//i[@class="newcarj"]/text()',),
                },
                'brand_slug': {
                    'xpath': ('//div[@class="autotit"]/strong/text()',),
                },
                'model_slug': {
                    'xpath': ('//div[@class="autotit"]/strong/text()',),
                },
                'city': {
                    'xpath': ('//div[@class="autotit"]/h2/text()',),
                    'processors': ['first', 'haoche51.city'],
                },
                'description': {
                    'xpath': (
                        '//p[@class="f-type03"]/text()',
                        '//div[@class="ow-sa"]/p[not(@class)]/text()'
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
                'phone': {
                    'xpath': ('//li[@class="tc-der"]/strong/text()',),
                },
                'mandatory_insurance': {
                    'xpath': (
                        u'//div[@class="ow-sa1"]/ul/li[contains(text(), "交强")]/text()',
                    ),
                },
                'business_insurance': {
                    'xpath': (
                        u'//div[@class="ow-sa1"]/ul/li[contains(text(), "商业")]/text()',
                    ),
                },
                'examine_insurance': {
                    'xpath': (
                        u'//div[@class="ow-sa1"]/ul/li[contains(text(), "年检")]/text()',
                    ),
                },
                'transfer_owner': {
                    'xpath': (
                        # '//li[@class="guohu"]/text()',
                        '//div[@class="autotit"]/h2/text()[1]',
                        '//div[@class="ow-sa"]/div/strong/text()',
                    ),
                    'processors': ['first', 'haoche51.transfer_owner'],
                    'default': 0,
                },
                'quality_service': {
                    'default': u' '.join([
                        u'1年/2万公里放心质保',
                        u'14天可退车',
                    ])
                },
                'source_type': {
                    'default': SOURCE_TYPE_SELLER,
                },
                'driving_license': {
                    'xpath': (
                        u'//li[contains(text(), "行驶证")]/text()',
                    ),
                    'processors': ['first', 'haoche51.driving_license'],
                },
                'invoice': {
                    'xpath': (
                        u'//li[contains(text(), "购车发票")]/text()',
                    ),
                    'processors': ['first', 'haoche51.invoice'],
                },
            },
        },
    },
}
# start_url = rule['start_urls'][0]
# if ('html' in start_url and len(start_url) > 40) \
#         or rule['parse']['url']['contains'][0] in start_url:
#     rule['parse'] = rule['parse_detail']
