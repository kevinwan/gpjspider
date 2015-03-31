# -*- coding: utf-8 -*-
"""
好车无忧优质二手车 规则

规则包含非 ascii 字符，必须使用 unicode 编码
"""


def format_func(url_str):
    """
    javascript:window.open('http://bj.haoche51.com/details/20003.html')
    """
    s = url_str.index("javascript:window.open('")
    if s >= 0:
        s += len("javascript:window.open('")
    else:
        return None
    if not url_str.endswith("')"):
        return None
    else:
        return url_str[s:-3]


rule = {
    #==========================================================================
    #  基本配置
    #==========================================================================
    'name': '优质二手车-好车无忧-规则',
    'domain': 'haoche51.com',
    'start_urls': ['http://bj.haoche51.com/vehicle_list.html'],

    #==========================================================================
    #  默认步骤  parse
    #==========================================================================
    'parse': {
        "url": {
            "xpath": ('//div[@class="contx"]/ul/li/a/@href',),
            "step": 'parse_list',
        }
    },
    #==========================================================================
    #  详情页步骤  parse_list
    #==========================================================================
    'parse_list': {
        "url": {
            "xpath": (
                ('//div[@class="content"]/div/div/@onclick',),
            ),
            "format": format_func,
            "step": 'parse_detail',
        },
        "next_page_url": {
            "xpath": (
                u'//a[contains(text(), "下一页")]/@href',
            ),
            "excluded": ("javscript",),
            # 新 url 对应的解析函数
            "step": 'parse_list',
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
                    'processors': ['first', 'strip'],
                    'required': True,
                },
                'meta': {
                    'xpath': (
                        '//meta[@name="Description"]/@content',
                        '//meta[@name="description"]/@content'
                    ),
                    'processors': ['first', 'strip'],
                },
                'year': {
                    'xpath': ('//div[@class="autotit"]/h2/text()',),
                    'processors': ['first', 'strip', 'year'],
                },
                'month': {
                    'xpath': ('//div[@class="autotit"]/h2/text()',),
                    'processors': ['first', 'strip'],
                },
                'mile': {
                    'xpath': ('//div[@class="autotit"]/h2/text()',),
                    'processors': ['first', 'strip', 'mile'],
                },
                'volume': {
                    'xpath': (
                        u'//li[contains(text(), "排量")]/following-sibling::li[1]/text()',
                    ),
                    'processors': ['first', 'strip'],
                },

                # 'color': {
                #     'xpath': (
                #         u'//th[contains(text(), "颜色")]/../td[not(@class)]/text()',
                #     ),
                #     'processors': ['first', 'strip'],
                # },
                'control': {
                    'xpath': ('//div[@class="autotit"]/h2/text()',),
                    'processors': ['first', 'strip'],
                },
                'price': {
                    'xpath': ('//div[@class="car-quotation"]/strong/text()',),
                    'processors': ['first', 'strip', 'price', 'gpjfloat'],
                },
                'price_bn': {
                    'xpath': ('//i[@class="newcarj"]/text()',),
                    'processors': ['first', 'strip', 'gpjfloat'],
                },
                'brand_slug': {
                    'xpath': ('//div[@class="autotit"]/strong/text()',),
                    'processors': ['first', 'strip', 'brand_slug'],
                },
                'model_slug': {
                    'xpath': ('//div[@class="autotit"]/strong/text()',),
                    'processors': ['first', 'strip', 'model_slug'],
                },
                'city': {
                    'xpath': ('//p[@class="own"]/text()',),
                    'processors': ['first', 'strip'],
                },
                'description': {
                    'xpath': ('//p[@class="f-type03"]/text()',),
                    'processors': ['join', 'strip'],
                },
                'imgurls': {
                    'xpath': ('//div[@class="dt-pictype"]/img/@data-original',),
                    'processors': ['join', 'strip'],
                },
                'mandatory_insurance': {
                    'xpath': ('//li[@class="baoxian"]/text()',),
                    'processors': ['first', 'strip'],
                },
                'examine_insurance': {
                    'xpath': ('//li[@class="nianjian"]/text()',),
                    'processors': ['first', 'strip'],
                },
                'transfer_owner': {
                    'xpath': ('//li[@class="guohu"]/text()',),
                    'processors': ['gpjint'],
                    'default': 0,
                },
            },
        },
    },
}
