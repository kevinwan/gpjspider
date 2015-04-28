# -*- coding: utf-8 -*-
"""
赶集好车优质二手车 规则

规则包含非 ascii 字符，必须使用 unicode 编码
"""
from gpjspider.utils.constants import SOURCE_TYPE_SELLER


rule = {
    #==========================================================================
    #  基本配置
    #==========================================================================
    'name': '优质二手车-赶集好车-规则',
    'domain': 'haoche.ganji.com',
    # start_urls  或者 start_url_template只能设置其一，
    # start_url_function 配合 start_url_template一起用
    #  start_url_function 必须返回一个生成器
    'start_urls': ['http://haoche.ganji.com'],

    #==========================================================================
    #  默认步骤  parse
    #==========================================================================
    'parse': {
        "url": {
            "xpath": ('//div[@class="c2city"]/ul/li/a/@href',),
            "format": "http://haoche.ganji.com{0}buy/",
            # 新 url 对应的解析函数
            "step": 'parse_list',
        }
    },
    #==========================================================================
    #  详情页步骤  parse_list
    #==========================================================================
    'parse_list': {
        "url": {
            "xpath": (
                '//ul[@class="list-bigimg clearfix"]/li/div/a/@href',
            ),
            "format": "http://haoche.ganji.com{0}",
            "step": 'parse_detail',
            'update': True,
            'category': 'usedcar'
        },
        "next_page_url": {
            "xpath": (
                '//a[@class="next"]/@href',
            ),
            "format": "http://haoche.ganji.com{0}",
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
                    'xpath': (
                        '//h1[@class="dt-titletype"]/text()',
                    ),
                    'processors': ['first', 'strip'],
                    'required': True,
                },
                'meta': {
                    'xpath': (
                        '//meta[@name="description"]/@content',
                        '//meta[@name="Description"]/@content',
                    ),
                    'processors': ['first', 'strip'],
                },
                'year': {
                    'xpath': ('//li[@class="one"]/b/text()',),
                    'processors': ['first', 'strip', 'year'],
                },
                'month': {
                    'xpath': ('//li[@class="one"]/b/text()',),
                    'processors': ['first', 'strip', 'month'],
                },
                'mile': {
                    'xpath': (u'//li[contains(text(), "里程")]/b/text()',),
                    'processors': ['first', 'strip', 'mile'],
                },
                'volume': {
                    'xpath': (u'//li[contains(text(), "排量")]/b/text()',),
                    'processors': ['first', 'strip', 'volume'],
                },
                'control': {
                    'xpath': (u'//li[contains(text(), "变速箱")]/b/text()',),
                    'processors': ['first', 'strip'],
                },
                'price': {
                    'xpath': ('//b[@class="f30 numtype"]/text()',),
                    'processors': ['first', 'strip', 'price'],
                },
                #  加上 price之后才是新车价
                'price_bn': {
                    'xpath': (
                        '//div[@class="pricebox"]/span[@class="f14"]/i/text()',
                    ),
                    'processors': ['first', 'strip', 'ganjihaoche.price_bn'],
                },
                'phone': {
                    'xpath': (
                        '//b[@class="teltype"]/text()',
                    ),
                    'processors': ['first', 'strip'],
                },
                'brand_slug': {
                    'xpath': (u'//span[contains(text(), "检测车型")]/text()',),
                    'processors': ['first', 'strip', 'ganjihaoche.brand_slug'],
                },
                'model_slug': {
                    'xpath': (u'//span[contains(text(), "检测车型")]/text()',),
                    'processors': ['first', 'strip', 'ganjihaoche.model_slug'],
                },
                'city': {
                    'xpath': (
                        '//a[@class="choose-city"]/span/text()',
                    ),
                    'processors': ['first', 'strip', 'city'],
                },
                'city_slug': {
                    'xpath': (
                        '//a[@class="toindex"]/@href',
                    ),
                    'processors': ['first', 'strip', 'ganjihaoche.city_slug'],
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
                    'processors': ['first', 'gpjint'],
                    'default': 0,
                },
                'quality_service': {
                    'xpath': (
                        '//ul[@class="indem-ul"]/li/p[@class]/text()',
                    ),
                    'processors': ['join', 'strip'],
                },
                'source_type': {
                    'default': SOURCE_TYPE_SELLER,
                },
            },
        },
    },
}
