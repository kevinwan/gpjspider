# -*- coding: utf-8 -*-
"""
58 厂商认证二手车(manufacturer_certificated_cars) 规则
"""
from gpjspider.utils.constants import SOURCE_TYPE_MANUFACTURER


rule = {
    #==========================================================================
    #  基本配置
    #==========================================================================
    'name': u'厂商认证二手车-58-规则',
    'domain': '58.com',
    'start_urls': [
        'http://volvo.58.com/ershouche/?sheng=quanguo&city=qg',
        'http://chengxin.58.com/ershouche/?sheng=quanguo&city=qg',
        'http://audi.58.com/ershouche/?renzheng=1&sheng=quanguo&city=qg',
        'http://sh.58.com/svwuc2sc/ershouche/',
        'http://yicheng.58.com/ershouche/?sheng=quanguo&city=qg',
        'http://longxin.58.com/ershouche/?sheng=quanguo&city=qg',
        # 喜悦二手车 虽然不提供全国搜索，但58还是提供了
        'http://ghac.58.com/ershouche/?sheng=quanguo&city=qg',
    ],

    #==========================================================================
    #  默认步骤  parse
    #==========================================================================
    'parse': {
        "url": {
            "xpath": ('//ul[@class="arealist"]/li/a/@href',),
            # 新 url 对应的解析函数
            "step": 'parse_detail',
            'update': True,
            'category': 'usedcar'
        },
        "next_page_url": {
            "xpath": ('//a[@class="next"]/@href', ),
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
                        '//h1[@class="h1"]/text()',
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
                    'xpath': (
                        u'//span[contains(text(), "上牌时间")]/following-sibling::span/text()',
                    ),
                    'processors': ['first', 'strip', 'year', 'gpjint'],
                },
                'month': {
                    'xpath': (
                        u'//span[contains(text(), "上牌时间")]/following-sibling::span/text()',
                    ),
                    'processors': ['first', 'strip', 'month', 'gpjint'],
                },
                'mile': {
                    'xpath': (
                        u'//span[contains(text(), "行驶里程")]/following-sibling::span/text()',
                    ),
                    'processors': ['first', 'strip', 'mile', 'decimal'],
                },
                'volume': {
                    'xpath': (
                        u'//span[contains(text(), "排量")]/following-sibling::span/text()',
                    ),
                    'processors': ['first', 'strip', 'volume'],
                },

                'color': {
                    'xpath': (
                        u'//span[contains(text(), "颜色")]/following-sibling::span/text()',
                    ),
                    'processors': ['first', 'strip'],
                },
                'control': {
                    'xpath': (
                        u'//span[contains(text(), "变速箱")]/following-sibling::span/text()',
                    ),
                    'processors': ['first', 'strip'],
                },
                'price': {
                    'xpath': (
                        '//span[@class="font_jiage"]/text()',
                    ),
                    'processors': ['first', 'strip', 'price'],
                },
                # 'price_bn': {
                #     'xpath': (
                #         '//p[@class="market-price"]/del/text()',
                #     ),
                #     'processors': ['first', 'strip', 'price_bn'],
                # },
                'brand_slug': {
                    'xpath': (
                        '//a[@id="carbrands"]/text()',
                    ),
                    'processors': ['first', 'strip'],
                },
                'model_slug': {
                    'xpath': (
                        '//a[@id="carseriess"]/text()',
                    ),
                    'processors': ['first', 'strip']
                },
                'city': {
                    'xpath': ('//meta[@name="location"]/@content',),
                    'processors': ['first', 'strip', '58.city'],
                },
                'region': {
                    'xpath': (
                        '//span[@id="address_detail"]/text()',
                    ),
                    'processors': ['first', 'strip'],
                },
                'phone': {
                    'xpath': (
                        '//*[@id="t_phone"][1]/text()',
                    ),
                    'processors': ['58.phone'],
                },
                'company_name': {
                    'xpath': (
                        '//span[@class="font_yccp"]/text()',
                    ),
                    'processors': ['first', 'strip'],
                },
                'company_url': {
                    'xpath': (
                        '//a[@class="dianpu_link"]/@href',
                    ),
                    'processors': ['first', 'strip'],
                },
                # 'driving_license': {
                #     'xpath': (
                #         u'//li/span[contains(text(), "行驶证")]/../text()',
                #     ),
                #     'processors': ['first', 'strip'],
                # },
                # 'invoice': {
                #     'xpath': (
                #         u'//li/span[contains(text(), "购车发票")]/../text()',
                #     ),
                #     'processors': ['first', 'strip'],
                # },
                'maintenance_record': {
                    'xpath': (
                        u'//span[contains(text(), "保养")]/following-sibling::span/text()',
                    ),
                    'processors': ['first', 'strip'],
                },
                'quality_service': {
                    'xpath': (
                        u'//*[@id="baozhang"]/span[@class="paddright13"]/text()',
                    ),
                    'processors': ['join', 'strip'],
                },

                'description': {
                    'xpath': ('//div[@class="benchepeizhi"]/span/text()',),
                    'processors': ['join', 'strip'],
                },
                'imgurls': {
                    'xpath': ('//img[@class="mb_4"]/@src',),
                    'processors': ['join', 'strip'],
                },
                'mandatory_insurance': {
                    'xpath': (
                        u'//span[contains(text(), "交强")]/following-sibling::span/text()',
                    ),
                    'processors': ['first', 'strip', 'mandatory_insurance'],
                },
                # 'business_insurance': {
                #     'xpath': (
                #         u'//li/span[contains(text(), "商业险到期时间")]/../text()',
                #     ),
                #     'processors': ['first', 'strip'],
                # },
                'examine_insurance': {
                    'xpath': (
                        u'//span[contains(text(), "年检")]/following-sibling::span/text()',
                    ),
                    'processors': ['first', 'strip'],
                },
                # 'transfer_owner': {
                #     'xpath': (
                #         u'//li/span[contains(text(), "是否一手车")]/../text()',
                #     ),
                #     'processors': ['first', 'strip', '99haoche.transfer_owner'],
                # },
                # 'car_application': {
                #     'xpath': (
                #         u'//li/span[contains(text(), "使用性质")]/../text()',
                #     ),
                #     'processors': ['first', 'strip'],
                # },
                # contact
                # condition_level
                # condition_detail
                #
                # maintenance_desc
                'source_type': {
                    'default': SOURCE_TYPE_MANUFACTURER,
                },
                'is_certifield_car': {
                    'xpath': (
                        u'//*[@id="baozhang"]/span[@class="paddright13"]/text()',
                    ),
                    'processors': ['first', 'strip', '58.is_certifield_car'],
                    'default': False,
                },
            },
        },
    },
}
