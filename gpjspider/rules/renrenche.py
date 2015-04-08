# -*- coding: utf-8 -*-
"""
人人车优质二手车 规则

规则包含非 ascii 字符，必须使用 unicode 编码
"""
from gpjspider.utils.constants import SOURCE_TYPE_SELLER


rule = {
    #==========================================================================
    #  基本配置
    #==========================================================================
    'name': '优质二手车-人人车-规则',
    'domain': 'renrenche.com',
    # start_urls  或者 start_url_template只能设置其一，
    # start_url_function 配合 start_url_template一起用
    #  start_url_function 必须返回一个生成器
    'start_urls': ['http://www.renrenche.com/'],

    #==========================================================================
    #  默认步骤  parse
    #==========================================================================
    'parse': {
        "url": {
            "xpath": ('//div[@id="cities"]/ul/li/a/@href',),
            "format": "http://www.renrenche.com{0}/ershouche",
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
                '//div[@class="container search-list-wrapper"]/ul/li/a/@href',
            ),
            "format": "http://www.renrenche.com{0}",
            "step": 'parse_detail',
        },
        "next_page_url": {
            "xpath": (
                '//a[text()=">"]/@href',
            ),
            "excluded": ('javascript'),
            "format": "http://www.renrenche.com{0}",
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
                        '//h1[@class="span19"]/text()',
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
                    'xpath': ('//li[@class="span7"][1]/p/strong/text()',),
                    'processors': ['first', 'strip', 'year'],
                },
                'month': {
                    'xpath': ('//li[@class="span7"][1]/p/strong/text()',),
                    'processors': ['first', 'strip', 'month'],
                },
                'mile': {
                    'xpath': ('//li[@class="span7"][2]/p/strong/text()',),
                    'processors': ['first', 'strip', 'mile'],
                },
                'volume': {
                    'xpath': (
                        u'//td[text()="发动机"]/following-sibling::td/text()',
                    ),
                    'processors': ['first', 'strip'],
                },

                'color': {
                    'xpath': (
                        u'//td[text()="车身颜色"]/following-sibling::td[1]/text()',
                    ),
                    'processors': ['first', 'strip'],
                },
                'control': {
                    'xpath': (
                        u'//td[text()="变速箱"]/following-sibling::td[@class]/text()',
                    ),
                    'processors': ['first', 'strip'],
                },
                'price': {
                    'xpath': ('//p[@class="box-price"]/text()',),
                    'processors': ['first', 'strip', 'price', 'gpjfloat'],
                },
                'price_bn': {
                    'xpath': (u'//li[contains(text(), "新车")]/text()',),
                    'processors': ['first', 'strip', 'price_bn'],
                },
                'brand_slug': {
                    'xpath': ('//h1[@class="span19"]/text()',),
                    'processors': ['first', 'strip', 'brand_slug'],
                },
                'model_slug': {
                    'xpath': ('//h1[@class="span19"]/text()',),
                    'processors': ['first', 'strip', 'model_slug'],
                },
                'city': {
                    'xpath': (
                        '//input[@id="intent_buy_city"]/@value',
                    ),
                    'processors': ['first', 'strip'],
                },
                'city_slug': {
                    'xpath': (
                        '//*[@id="div_city"]/a/@href',
                    ),
                    'processors': ['first', 'strip', 'renrenche.city_slug'],
                },
                'region': {
                    'xpath': (
                        '//div[@class="text-block bottom-right"]/h3/text()',
                    ),
                    'processors': ['first', 'strip', 'renrenche.region'],
                },
                'description': {
                    'xpath': (
                        '//div[@class="main"]/div/p/text()',
                    ),
                    'processors': ['join', 'strip'],
                },
                'thumbnail': {
                    'xpath': (
                        '//div[@class="detail-box-bg"]/img/@src',
                    ),
                    'processors': ['first', 'strip', 'strip_url'],
                },
                'imgurls': {
                    'xpath': (
                        '//div[@class="container detail-gallery"]/div//img/@src',
                        '//div[@class="detail-box-bg"]/img/@src',
                    ),
                    'processors': ['join', 'strip', 'strip_imgurls'],
                },
                'mandatory_insurance': {
                    'xpath': (
                        u'//td[contains(text(), "交强险")]/following-sibling::td[1]/text()',
                    ),
                    'processors': ['first', 'strip'],
                },
                'examine_insurance': {
                    'xpath': (
                        u'//td[contains(text(), "年检")]/following-sibling::td[1]/text()',
                    ),
                    'processors': ['first', 'strip'],
                },
                'transfer_owner': {
                    'xpath': (
                        u'//td[contains(text(), "过户")]/following-sibling::td[1]/text()',
                    ),
                    'processors': ['gpjint'],
                    'default': 0,
                },
                'quality_service': {
                    'xpath': (
                        u'//td[contains(text(), "服务项")]/following-sibling::td//td/text()[2]',
                    ),
                    'processors': ['join', 'strip'],
                    'default': 0,
                },
                'phone': {
                    'xpath': (
                        '//span[@class="tel span4"]/img/@alt',
                    ),
                    'processors': ['join', 'strip'],
                },
                'contact': {
                    'default': u'人人车客服',
                },
                'condition_detail': {
                    'xpath': (
                        '//span[@class="desc"]/text()',
                    ),
                    'processors': ['join', 'strip'],
                },
                'condition_level': {
                    'xpath': (
                        '//span[@class="desc"]/text()',
                    ),
                    'processors': ['first', 'strip', 'renrenche.cond_level'],
                },
                'invoice': {
                    'xpath': (
                        u'//td[contains(text(), "购车发票")]/following-sibling::td[1]/text()',
                    ),
                    'processors': ['first', 'strip'],
                },
                'maintenance_record': {
                    'xpath': (
                        u'//td[contains(text(), "4S店保养")]/following-sibling::td[1]/text()',
                    ),
                    'processors': ['first', 'strip'],
                },
                'dmodel': {
                    'xpath': (
                        '//h1[@class="span19"]/text()',
                    ),
                    'processors': ['first', 'strip'],
                },
                'source_type': {
                    'default': SOURCE_TYPE_SELLER,
                },
            },
        },
    },
}
