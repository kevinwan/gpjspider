# -*- coding: utf-8 -*-
"""
优信二手车
"""
from gpjspider.utils.constants import SOURCE_TYPE_SELLER


rule = {
    #==========================================================================
    #  基本配置
    #==========================================================================
    'name': u'优质二手车-优信-规则',
    'domain': 'xin.com',
    # start_urls  或者 start_url_template只能设置其一，
    # start_url_function 配合 start_url_template一起用
    #  start_url_function 必须返回一个生成器
    'start_urls': ['http://www.xin.com/quanguo/s/o2a2i1v1/'],

    #==========================================================================
    #  默认步骤  parse
    #==========================================================================
    'parse': {
        "url": {
            "xpath": ('//div[@class="car-box clearfix"]/div/div/p/a/@href',),
            "format": "http://www.xin.com{0}",
            # 新 url 对应的解析函数
            "step": 'parse_detail',
        },
        "next_page_url": {
            "xpath": (
                u'//a[contains(text(), "下一页")]/@data-page',
            ),
            "format": 'http://www.xin.com/quanguo/s/o2a2i{0}v1/',
            # 新 url 对应的解析函数
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
                    'xpath': ('//div[@class="tit"]/h1/text()',),
                    'processors': ['first', 'strip'],
                    'required': True,
                },
                'meta': {
                    'xpath': ('//meta[@name="description"]/@content',),
                    'processors': ['strip', 'join'],
                    'required': True,
                },
                'year': {
                    'xpath': (u'//li[@class="br"]/span[contains(text(), "上牌时间")]/../em/text()',),
                    'processors': ['first', 'strip', 'year'],
                },
                'month': {
                    'xpath': (u'//li[@class="br"]/span[contains(text(), "上牌时间")]/../em/text()',),
                    'processors': ['first', 'strip', 'month'],
                },
                'mile': {
                    'xpath': (u'//li[@class="br"]/span[contains(text(), "行驶里程")]/../em/text()',),
                    'processors': ['first', 'strip', 'mile', 'gpjfloat'],
                },
                'volume': {
                    'xpath': (u'//li[@class="br"]/span[contains(text(), "排量")]/../em/text()',),
                    'processors': ['first', 'strip'],
                },

                'color': {
                    'xpath': (u'//td[contains(text(), "颜色")]/following-sibling::td/text()',),
                    'processors': ['first', 'strip'],
                },
                'control': {
                    'xpath': (u'//td[contains(text(), "变速箱")]/following-sibling::td/text()',),
                    'processors': ['first', 'strip'],
                },
                'region': {
                    'xpath': (
                        '//div[@class="company"]/p[2]/text()',
                    ),
                    'processors': ['first', 'strip'],
                },
                'price': {
                    'xpath': (u'//div[@class="wan_1"]/em/text()',),
                    'processors': ['first', 'price', 'decimal'],
                },
                'price_bn': {
                    'xpath': (u'//div[@class="wan_2"]/span/del/text()',),
                    'processors': ['first', 'strip', 'decimal'],
                },
                'brand_slug': {
                    'xpath': ('//div[@class="tit"]/h1/text()',),
                    'processors': ['first', 'strip', 'brand_slug'],
                },
                'model_slug': {
                    'xpath': ('//div[@class="tit"]/h1/text()',),
                    'processors': ['first', 'strip', 'model_slug'],
                },
                'city': {
                    'xpath': (u'//li/span[contains(text(), "销售城市")]/../em/text()',),
                    'processors': ['first', 'strip'],
                },
                'description': {
                    'xpath': (u'//div[@class="test-report"]/div[@class="test-txt"]/ul/li/text()',),
                    'processors': ['join', 'strip'],
                },
                'imgurls': {
                    'xpath': ('//div[@class="carimg"]/div/img/@src',),
                    'processors': ['join', 'strip'],
                },
                'mandatory_insurance': {
                    'xpath': (u'//td[contains(text(), "保险到期时间")]/following-sibling::td/text()',),
                    'processors': ['first', 'strip'],
                },
                'company_name': {
                    'xpath': ('//div[@class="newcompany"]/p/text()',),
                    'processors': ['first', 'strip'],
                },
                'company_url': {
                    'xpath': ('//div[@class="newcompany"]/a/@href',),
                    'processors': ['first', 'strip', 'xin.company_url'],
                },
                'examine_insurance': {
                    'xpath': (
                        u'//td[contains(text(), "年检有效期")]/following-sibling::td/text()',
                    ),
                    'processors': ['first', 'strip'],
                },
                'transfer_owner': {
                    'xpath': (
                        u'//td[contains(text(), "过户次数")]/following-sibling::td/text()',
                    ),
                    'processors': ['first', 'strip', 'xin.transfer_owner'],
                },
                'quality_service': {
                    'xpath': ('//div[@class="day-pic"]/img/@src',),
                    'default': u'无',
                    'processors': ['first', 'xin.quality_service']
                },
                'source_type': {
                    'default': SOURCE_TYPE_SELLER,
                },
            },
        },
    },
}
