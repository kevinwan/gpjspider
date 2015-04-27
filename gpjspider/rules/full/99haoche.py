# -*- coding: utf-8 -*-
"""
99好车 优质二手车 规则
"""
from gpjspider.utils.constants import SOURCE_TYPE_SELLER


rule = {
    #==========================================================================
    #  基本配置
    #==========================================================================
    'name': u'优质二手车-99好车-规则',
    'domain': '99haoche.com',
    'start_urls': ['http://www.99haoche.com/quanguo/all/?p=v1'],

    #==========================================================================
    #  默认步骤  parse
    #==========================================================================
    'parse': {
        "url": {
            "re": (r'http://www\.99haoche\.com/car/\d+\.html',),
            # 新 url 对应的解析函数
            "step": 'parse_detail',
            'update': True,
            'category': 'usedcar'
        },
        "next_page_url": {
            "xpath": ('//a[@id="pagenow"]/following-sibling::a[1]/@href', ),
            'format': 'http://www.99haoche.com{0}',
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
                        u'//li/span[contains(text(), "首次上牌")]/../span[@class="righ"]/text()',
                    ),
                    'processors': ['first', 'strip', 'year', 'gpjint'],
                },
                'month': {
                    'xpath': (
                        u'//li/span[contains(text(), "首次上牌")]/../span[@class="righ"]/text()',
                    ),
                    'processors': ['first', 'strip', 'month', 'gpjint'],
                },
                'mile': {
                    'xpath': (
                        u'//li/span[contains(text(), "行驶里程")]/../span[@class="righ"]/text()',
                    ),
                    'processors': ['first', 'strip', 'mile', 'decimal'],
                },
                'volume': {
                    'xpath': (
                        '//div[@class="car-particular-right clearfix"]/h2/text()',
                    ),
                    'processors': ['first', 'strip', 'volume'],
                },

                'color': {
                    'xpath': (u'//li/span[contains(text(), "车身颜色")]/../text()',),
                    'processors': ['first', 'strip', '99haoche.color'],
                },
                'control': {
                    'xpath': (
                        u'//li/span[contains(text(), "变速方式")]/../span[@class="righ"]/text()',
                    ),
                    'processors': ['first', 'strip'],
                },
                'price': {
                    'xpath': (
                        '//p[@class="market-price"]/span[@class="str"]/text()',
                    ),
                    'processors': ['first', 'strip', 'price'],
                },
                'price_bn': {
                    'xpath': (
                        '//p[@class="market-price"]/del/text()',
                    ),
                    'processors': ['first', 'strip', 'price_bn'],
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
                    'processors': ['first', 'strip', 'city'],
                },
                'region': {
                    'xpath': (
                        u'//span[contains(text(), "看车地址")]/following-sibling::span/text()',
                    ),
                    'processors': ['first', 'strip'],
                },
                'phone': {
                    'xpath': (
                        '//a[@name="showPhone2"]/text()',
                    ),
                    'processors': ['first', 'strip'],
                },
                'company_name': {
                    'xpath': (
                        u'//span[contains(text(), "所属商家")]/following-sibling::a/text()',
                    ),
                    'processors': ['first', 'strip'],
                },
                'company_url': {
                    'xpath': (
                        u'//span[contains(text(), "所属商家")]/following-sibling::a/@href',
                    ),
                    'processors': ['first', 'strip'],
                },
                'driving_license': {
                    'xpath': (
                        u'//li/span[contains(text(), "行驶证")]/../text()',
                    ),
                    'processors': ['first', 'strip'],
                },
                'invoice': {
                    'xpath': (
                        u'//li/span[contains(text(), "购车发票")]/../text()',
                    ),
                    'processors': ['first', 'strip'],
                },
                'maintenance_record': {
                    'xpath': (
                        u'//li/span[contains(text(), "保养记录")]/../text()',
                    ),
                    'processors': ['first', 'strip'],
                },
                # 'quality_service': {
                #     'xpath': (
                #         u'//div[@class="diverse-serve"]/p/a/text()',
                #     ),
                #     'processors': ['join', 'strip'],
                # },
                'is_certifield_car': {
                    'default': 1,
                },
                'description': {
                    'xpath': ('//div[@class="postscript"]/p[1]/text()',),
                    'processors': ['first', 'strip'],
                },
                'imgurls': {
                    'xpath': ('//ul[@id="img_R_L_List"]/li/a/img/@src',),
                    'processors': ['join', 'strip'],
                },
                'mandatory_insurance': {
                    'xpath': (
                        u'//li/span[contains(text(), "交强险到期时间")]/../text()',
                    ),
                    'processors': ['first', 'strip'],
                },
                'business_insurance': {
                    'xpath': (
                        u'//li/span[contains(text(), "商业险到期时间")]/../text()',
                    ),
                    'processors': ['first', 'strip'],
                },
                'examine_insurance': {
                    'xpath': (
                        u'//td[contains(text(), "年检有效期")]/following-sibling::td/text()',
                    ),
                    'processors': ['first', 'strip'],
                },
                'transfer_owner': {
                    'xpath': (
                        u'//li/span[contains(text(), "是否一手车")]/../text()',
                    ),
                    'processors': ['first', 'strip', '99haoche.transfer_owner'],
                },
                'source_type': {
                    'default': SOURCE_TYPE_SELLER,
                },
                'car_application': {
                    'xpath': (
                        u'//li/span[contains(text(), "使用性质")]/../text()',
                    ),
                    'processors': ['first', 'strip'],
                },
                # contact
                # condition_level
                # condition_detail
                # 
                # maintenance_desc
            },
        },
    },
}
