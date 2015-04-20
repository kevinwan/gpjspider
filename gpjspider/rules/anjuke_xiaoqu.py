# -*- coding: utf-8 -*-
"""
安居客小区 规则

规则包含非 ascii 字符，必须使用 unicode 编码
"""
from gpjspider.utils.constants import SOURCE_TYPE_SELLER


rule = {
    #==========================================================================
    #  基本配置
    #==========================================================================
    'name': '小区-安居客-规则',
    'domain': 'anjuke.com',
    # start_urls  或者 start_url_template只能设置其一，
    # start_url_function 配合 start_url_template一起用
    #  start_url_function 必须返回一个生成器
    'start_urls': ['http://www.anjuke.com/index.html'],

    #==========================================================================
    #  默认步骤  parse
    #==========================================================================
    'parse': {
        "url": {
            "xpath": ('//div[@class="cities_boxer"]//dd/a/@href',),
            'format': "{0}/community/",
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
                '//ul[@class="list"]/li/a/@href',
            ),
            "step": 'parse_detail',
        },
        "next_page_url": {
            "xpath": (
                '//a[@class="aNxt"]/@href',
            ),
            # 新 url 对应的解析函数
            "step": 'parse_list',
        },
    },

    #==========================================================================
    #  详情页步骤  parse_detail
    #==========================================================================
    'parse_detail': {
        "item": {
            "class": "CommunityItem",
            "fields": {
                'title': {
                    'xpath': ('//div[@class="comm-cont"]/h1/text()',),
                    'processors': ['first', 'strip'],
                    'required': True,
                },
                'avg_price': {
                    'xpath': ('//em[@class="comm-avg-price"]/text()',),
                    'processors': ['first', 'strip', 'decimal'],
                },
                'tags': {
                    'xpath': ('//div[@class="comm-mark clearfix"]/a/text()',),
                    'processors': ['join', 'strip'],
                },
                # 总面积
                'all_area': {
                    'xpath': (
                        u'//dl[@class="comm-r-detail float-r"]/dt[contains(text(), "总建面")]/following-sibling::dd[1]/text()',
                    ),
                    'processors': ['first', 'strip'],
                },
                # 
                'all_house': {
                    'xpath': (
                        u'//dl[@class="comm-r-detail float-r"]/dt[contains(text(), "总户数")]/following-sibling::dd[1]',
                    ),
                    'processors': ['first', 'strip'],
                },
                'build_time': {
                    'xpath': (
                        u'//dl[@class="comm-r-detail float-r"]/dt[contains(text(), "建造年代")]/following-sibling::dd[1]',
                    ),
                    'processors': ['first', 'strip'],
                },
                #  容积率
                'volume_ratio': {
                    'xpath': (
                        u'//dl[@class="comm-r-detail float-r"]/dt[contains(text(), "容积率")]/following-sibling::dd[1]',
                    ),
                    'processors': ['first', 'strip', 'decimal'],
                },
                #  停车位
                'parking_num': {
                    'xpath': (
                        u'//dl[@class="comm-r-detail float-r"]/dt[contains(text(), "停车位")]/following-sibling::dd[1]',
                    ),
                    'processors': ['first', 'strip', 'decimal'],
                },
                #  绿化率(%)
                'green_rate': {
                    'xpath': (
                        u'//dl[@class="comm-r-detail float-r"]/dt[contains(text(), "绿化率")]/following-sibling::dd[1]',
                    ),
                    'processors': ['first', 'strip', 'decimal'],
                },
                #  物业费
                'owner_property': {
                    'xpath': (
                        u'//dl[@class="comm-l-detail float-l"]/dt[contains(text(), "物业费用")]/following-sibling::dd[1]/text()',
                    ),
                    'processors': ['first', 'strip', 'decimal'],
                },
                #  物业类型
                'owner_type': {
                    'xpath': (
                        u'//dl[@class="comm-l-detail float-l"]/dt[contains(text(), "物业类型")]/following-sibling::dd[1]/text()',
                    ),
                    'processors': ['first', 'strip'],
                },
                #  物业公司
                'owner_type': {
                    'xpath': (
                        u'//dl[@class="comm-l-detail float-l"]/dt[contains(text(), "物业公司")]/following-sibling::dd[1]/text()',
                    ),
                    'processors': ['first', 'strip'],
                },
                #  开发商
                'owner_type': {
                    'xpath': (
                        u'//dl[@class="comm-l-detail float-l"]/dt[contains(text(), "开发商")]/following-sibling::dd[1]/text()',
                    ),
                    'processors': ['first', 'strip'],
                },
                'address': {
                    'xpath': (
                        u'//dl[@class="comm-l-detail float-l"]/dt[contains(text(), "地址")]/following-sibling::dd[1]/em/text()',
                    ),
                    'processors': ['first', 'strip'],
                },
                #  所在版块
                'in_area': {
                    'xpath': (
                        u'//dl[@class="comm-l-detail float-l"]/dt[contains(text(), "版块")]/following-sibling::dd[1]/a/text()',
                    ),
                    'processors': ['join', 'strip'],
                },
                #  描述
                'in_area': {
                    'xpath': (
                        u'//div[@class="desc-cont"]/text()',
                    ),
                    'processors': ['join', 'strip'],
                },
                
            },
        },
    },
}
