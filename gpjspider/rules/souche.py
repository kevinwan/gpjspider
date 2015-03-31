# -*- coding: utf-8 -*-
"""
大搜车优质二手车 规则


规则包含非 ascii 字符，必须使用 unicode 编码
"""
rule = {
    #==========================================================================
    #  基本配置
    #==========================================================================
    'name': '优质二手车-大搜车-规则',
    'domain': 'souche.com',
    # start_urls  或者 start_url_template只能设置其一，
    # start_url_function 配合 start_url_template一起用
    #  start_url_function 必须返回一个生成器
    'start_urls': ['http://www.souche.com'],

    #==========================================================================
    #  默认步骤  parse
    #==========================================================================
    'parse': {
        "url": {
            "xpath": ('//div[@class="area-line"]/a/@data-pinyin',),
            "format": "http://www.souche.com/{0}/list",
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
                ('//div[@class="card-box clearfix car-wrap "]'
                    '/div/a[@class="car-link"]/@href'),
            ),
            "format": "http://www.souche.com{0}",
            "step": 'parse_detail',
        },
        "next_page_url": {
            "xpath": (
                '//a[@class="next"]/@href',
            ),
            "format": "http://www.souche.com{0}",
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
                        '//div[@class="detail_main_info"]/div/h1/ins/text()',
                    ),
                    'processors': ['first', 'strip'],
                    'required': True,
                },
                'meta': {
                    'xpath': ('//meta[@name="Description"]/@content',),
                    'processors': ['first', 'strip'],
                },
                'year': {
                    'xpath': (
                        '//div[@class="car_detail clearfix"]/div[1]/strong/text()',
                    ),
                    'processors': ['first', 'strip', 'year'],
                },
                'month': {
                    'xpath': (
                        '//div[@class="car_detail clearfix"]/div[1]/strong/text()',
                    ),
                    'processors': ['first', 'strip', 'month'],
                },
                'mile': {
                    'xpath': (
                        '//div[@class="car_detail clearfix"]/div[2]/strong/text()',
                    ),
                    'processors': ['first', 'strip', 'mile'],
                },
                'volume': {
                    'xpath': (
                        u'//th[contains(text(), "排量")]/../td[not(@class)]/text()',
                    ),
                    'processors': ['first', 'strip'],
                },

                'color': {
                    'xpath': (
                        u'//th[contains(text(), "颜色")]/../td[not(@class)]/text()',
                    ),
                    'processors': ['first', 'strip'],
                },
                'control': {
                    'xpath': (
                        u'//th[contains(text(), "变速箱")]/../td[not(@class)]/text()',
                    ),
                    'processors': ['first', 'strip'],
                },
                'price': {
                    'xpath': (
                        '//div[@class="detail_price_left clearfix"]/em/text()',
                    ),
                    'processors': ['first', 'strip', 'price', 'gpjfloat'],
                },
                'price_bn': {
                    'xpath': ('//label[@class="new"]/text()',),
                    'processors': ['first', 'strip', 'price_bn'],
                },
                'brand_slug': {
                    'xpath': ('//div[@class="detail-map"]/a[last()-1]/text()',),
                    'processors': ['first', 'strip', 'brand_slug'],
                },
                'model_slug': {
                    'xpath': ('//div[@class="detail-map"]/a[last()]/text()',),
                    'processors': ['first', 'strip', 'model_slug'],
                },
                'city': {
                    'xpath': (
                        '//div[@class="item"][3]/strong/text()',
                    ),
                    'processors': ['first', 'strip'],
                },
                'description': {
                    'xpath': (
                        '//div[@class="sub_title"]/text()',
                    ),
                    'processors': ['join', 'strip'],
                },
                'imgurls': {
                    'xpath': (
                        '//ul[@class="photosSmall"]/li/img/@data-original',
                    ),
                    'processors': ['join', 'strip'],
                },
                # 'mandatory_insurance': {
                #     'xpath': (
                #         u'//td[contains(text(), "保险到期时间")]/following-sibling::td/text()',
                #     ),
                #     'processors': ['first', 'strip'],
                # },
                # 'examine_insurance': {
                #     'xpath': (
                #         u'//td[contains(text(), "年检有效期")]/following-sibling::td/text()',
                #     ),
                #     'processors': ['first', 'strip'],
                # },
                'transfer_owner': {
                    'xpath': (
                        u'//p[@class="record-num"]/../table/tbody/tr',
                    ),
                    'processors': ['souche.transfer_owner'],
                    'default': 0,
                },
            },
        },
    },
}
