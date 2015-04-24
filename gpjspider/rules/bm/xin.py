# -*- coding: utf-8 -*-

rule = {
    # ==========================================================================
    # config 基本配置
    # ==========================================================================
    'name': u'brand_model.xin',
    'domain': 'xin.com',
    # start_urls  或者 start_url_template只能设置其一，
    # start_url_function 配合 start_url_template一起用
    # start_url_function 必须返回一个生成器
    'start_urls': [
        'http://www.xin.com/chengdu/s/',
    ],

    # ==========================================================================
    # parse 默认步骤
    # ==========================================================================
    'parse': {
        'items': {
            'class': 'BrandModelItem',
            'xpath': '//ul[@class="brand-cars"]//a[@data-valueid]',
            'fields': {
                'url': {
                    'xpath': ('@data-valueid',),
                    'format': u'http://www.xin.com/chengdu/s/b{0}o2a2i1v1/',
                    'processors': ['first', 'strip'],
                    'required': True,
                },
                'name': {
                    'xpath': ('text()',),
                    'processors': ['first', 'strip'],
                    'required': True,
                },
                'slug': {
                    'xpath': ('@data-valueid',),
                    'processors': ['first', 'strip'],
                    'required': True,
                },
            }
        },
        'url': {
            'xpath': ('//ul[@class="brand-cars"]//a[@data-valueid]/@data-valueid',),
            'format': u'http://www.xin.com/chengdu/s/b{0}o2a2i1v1/',
            'step': 'parse_list',
        },
    },
    # ==========================================================================
    # parse_list 列表页步骤
    # ==========================================================================
    'parse_list': {
        'items': {
            'class': 'BrandModelItem',
            'xpath': '//div[@id="search_serial"]//td/a[@data-valueid]',
            'fields': {
                'name': {
                    'xpath': ('text()',),
                    'processors': ['first', 'strip'],
                    'required': True,
                },
                'slug': {
                    'xpath': ('@data-valueid',),
                    'processors': ['first', 'strip'],
                    'required': True,
                },
                'mum': {
                    'xpath': ('ancestor::tr/th/em/text()',),
                    'processors': ['first', 'strip'],
                },
                'parent': {
                    'xpath': ('//div[contains(@class, "sub-brand")]//a[contains(@class, "TipBtn TipBtn_hidden_b")]/text()',),
                    'processors': ['first', 'strip'],
                    'required': True,
                },
            }
        },
    },
}
