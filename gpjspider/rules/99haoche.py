# -*- coding: utf-8 -*-
"""
99好车 优质二手车 规则
"""
rule = {
    #==========================================================================
    #  基本配置
    #==========================================================================
    'name': u'优质二手车-99好车-规则',
    'domain': '99haoche.iautos.cn',
    'start_urls': ['http://quanguo.99haoche.iautos.cn/all/list/'],

    #==========================================================================
    #  默认步骤  parse
    #==========================================================================
    'parse': {
        "url": {
            "xpath": ('//ul[@class="bigpic clearfix"]/li/div/a/@href',),
            "excluded": ('99haoche.iautos.cn/s',),
            # 新 url 对应的解析函数
            "step": 'parse_detail',
        },
        "next_page_url": {
            "xpath": ('//a[@id="pagenow"]/following-sibling::a[1]/@href', ),
            "step": 'parse',
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
                        '//div[@class="car-particular-right clearfix"]/h2/text()',
                    ),
                    'processors': ['first', 'strip'],  # 处理器
                    'required': True,   # 默认为 False
                },
                'meta': {
                    'xpath': ('//meta[@name="description"]/@content',),
                    'processors': ['first', 'strip'],  # 处理器
                },
                'year': {
                    'xpath': (
                        u'//li/span[contains(text(), "首次上牌")]/../span[@class="righ"]/text()',
                    ),
                    'processors': ['first', 'strip', 'year'],  # 处理器
                },
                'month': {
                    'xpath': (
                        u'//li/span[contains(text(), "首次上牌")]/../span[@class="righ"]/text()',
                    ),
                    'processors': ['first', 'strip', 'month'],  # 处理器
                },
                'mile': {
                    'xpath': (
                        u'//li/span[contains(text(), "行驶里程")]/../span[@class="righ"]/text()',
                    ),
                    'processors': ['first', 'strip', 'mile'],  # 处理器
                },
                'volume': {
                    'xpath': (
                        '//div[@class="car-particular-right clearfix"]/h2/text()',
                    ),
                    'processors': ['first', 'strip'],  # 处理器
                },

                'color': {
                    'xpath': (u'//li/span[contains(text(), "车身颜色")]/../text()',),
                    'processors': ['first', 'strip'],  # 处理器
                },
                'control': {
                    'xpath': (
                        u'//li/span[contains(text(), "变速方式")]/../span[@class="righ"]/text()',
                    ),
                    'processors': ['first', 'strip'],  # 处理器
                },
                'price': {
                    'xpath': (
                        '//p[@class="market-price"]/span[@class="str"]/text()',
                    ),
                    'processors': ['first', 'strip', 'gpjfloat'],
                },
                'price_bn': {
                    'xpath': (
                        '//p[@class="market-price"]/del/text()',
                    ),
                    'processors': ['first', 'strip', 'price', 'gpjfloat'],
                },
                'brand_slug': {
                    'xpath': (
                        u'//li/span[contains(text(), "品牌车系")]/../span[@class="righ"]/text()',
                    ),
                    'processors': ['first', 'strip', 'brand_slug'],
                },
                'model_slug': {
                    'xpath': (
                        u'//li/span[contains(text(), "品牌车系")]/../span[@class="righ"]/text()',
                    ),
                    'processors': ['first', 'strip', 'model_slug']
                },
                'city': {
                    'xpath': (u'//h2[@name="location"]/a[2]/text()',),
                    'processors': ['first', 'strip'],  # 处理器
                },
                'description': {
                    'xpath': ('//div[@class="postscript"]/p[1]/text()',),
                    'processors': ['first', 'strip'],  # 处理器
                },
                'imgurls': {
                    'xpath': ('//ul[@id="img_R_L_List"]/li/a/img/@src',),
                    'processors': ['join', 'strip'],  # 处理器
                },
                'mandatory_insurance': {
                    'xpath': (
                        u'//li/span[contains(text(), "交强险到期时间")]/../text()',
                    ),
                    'processors': ['first', 'strip'],  # 处理器
                },
                'business_insurance': {
                    'xpath': (
                        u'//li/span[contains(text(), "商业险到期时间")]/../text()',
                    ),
                    'processors': ['first', 'strip'],  # 处理器
                },
                'examine_insurance': {
                    'xpath': (
                        u'//td[contains(text(), "年检有效期")]/following-sibling::td/text()',
                    ),
                    'processors': ['first', 'strip'],  # 处理器
                },
                'transfer_owner': {
                    'xpath': (
                        u'//td[contains(text(), "过户次数")]/following-sibling::td/text()',
                    ),
                    'processors': ['first', 'strip'],  # 处理器
                },
            },
        },
    },
}
