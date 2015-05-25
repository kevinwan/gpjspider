# -*- coding: utf-8 -*-
from .utils import *


rule = {
    'name': u'58同城',
    'domain': '58.com',
    'base_url': 'http://quanguo.58.com',
    'start_urls': [
        'http://quanguo.58.com/ershouche/',
        # 'http://sh.58.com/ershouche/22084792065823x.shtml',
        # 'http://quanguo.58.com/ershouche/0/',
        # 'http://quanguo.58.com/ershouche/1/',
        # 'http://quanguo.58.com/ershouche/?xbsx=1',
        # 'http://zz.58.com/ershouche/21565415848484x.shtml',
        # 'http://sy.58.com/ershouche/21851847601184x.shtml',
    ],

    'parse': {
        "url": {
            'xpath': (
                url('*[@id="infolist"]//*[@sortid]/'),
            ),
            # "re": (r'http.*58.com/ershouche/.*\.shtml',),
            'contains': ['/ershouche/'],
            "step": 'parse_detail',
            # 'update': True,
            # 'category': 'usedcar'
        },
        "next_page_url": {
            "xpath": (
                url(with_cls('list-tabs')),
                '//a[@class="next"]/@href',
            ),
            'format': True,
            "step": 'parse',
            'max_pagenum': 15,
            'incr_pageno': 8,
        },
    },

    'parse_detail': {
        "item": {
            "class": "UsedCarItem",
            "fields": {
                'title': {
                    'xpath': (
                        '//h1[@class="h1"]/text()',
                    ),
                    'required': True,
                },
                'meta': {
                    'xpath': (
                        '//meta[@name="description"]/@content',
                        '//meta[@name="Description"]/@content',
                    ),
                },
                'year': {
                    'xpath': (
                        u'//span[contains(text(), "上牌时间")]/following-sibling::span/text()',
                    ),
                },
                'month': {
                    'xpath': (
                        u'//span[contains(text(), "上牌时间")]/following-sibling::span/text()',
                    ),
                },
                'mile': {
                    'xpath': (
                        u'//span[contains(text(), "行驶里程")]/following-sibling::span/text()',
                    ),
                },
                'volume': {
                    'xpath': (
                        u'//span[contains(text(), "排量")]/following-sibling::span/text()',
                    ),
                },
                'color': {
                    'xpath': (
                        u'//span[contains(text(), "颜色")]/following-sibling::span/text()',
                    ),
                },
                'control': {
                    'xpath': (
                        u'//span[contains(text(), "变速箱")]/following-sibling::span/text()',
                    ),
                },
                'price': {
                    'xpath': (
                        '//span[@class="font_jiage"]/text()',
                    ),
                },
                # 'price_bn': {
                #     'xpath': (
                #         '//p[@class="market-price"]/del/text()',
                #     ),
                # },
                'brand_slug': {
                    'xpath': (
                        '//a[@id="carbrands"]/text()',
                    ),
                },
                'model_slug': {
                    'xpath': (
                        '//a[@id="carseriess"]/text()',
                    ),
                },
                'city': {
                    'xpath': ('//meta[@name="location"]/@content',),
                    'processors': ['first', '58.city'],
                },
                'region': {
                    'xpath': (
                        '//span[@id="address_detail"]/text()',
                    ),
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
                },
                'company_url': {
                    'xpath': (
                        '//a[@class="dianpu_link"]/@href',
                    ),
                },
                # 'driving_license': {
                #     'xpath': (
                #         u'//li/span[contains(text(), "行驶证")]/../text()',
                #     ),
                # },
                # 'invoice': {
                #     'xpath': (
                #         u'//li/span[contains(text(), "购车发票")]/../text()',
                #     ),
                # },
                'maintenance_record': {
                    'xpath': (
                        u'//span[contains(text(), "保养")]/following-sibling::span/text()',
                    ),
                },
                'quality_service': {
                    'xpath': (
                        u'//*[@id="baozhang"]/span[@class="paddright13"]/text()',
                    ),
                    'processors': ['join'],
                },

                'description': {
                    'xpath': ('//div[@class="benchepeizhi"]/span/text()',),
                    'processors': ['join'],
                },
                'imgurls': {
                    'xpath': ('//img[@class="mb_4"]/@src',),
                    'processors': ['join'],
                },
                'mandatory_insurance': {
                    'xpath': (
                        u'//span[contains(text(), "交强")]/following-sibling::span/text()',
                    ),
                },
                # 'business_insurance': {
                #     'xpath': (
                #         u'//li/span[contains(text(), "商业险到期时间")]/../text()',
                #     ),
                # },
                'examine_insurance': {
                    'xpath': (
                        u'//span[contains(text(), "年检")]/following-sibling::span/text()',
                    ),
                },
                # 'transfer_owner': {
                #     'xpath': (
                #         u'//li/span[contains(text(), "是否一手车")]/../text()',
                #     ),
                # },
                # 'car_application': {
                #     'xpath': (
                #         u'//li/span[contains(text(), "使用性质")]/../text()',
                #     ),
                # },
                # maintenance_desc
                'source_type': {
                    'xpath': (
                        # 厂商认证
                        'boolean(//div[@class="rz_biaozhi"])',
                        # 优质商家
                        '//*[@id="baozhang"]/span[@class="paddright13"]/text()',
                        # 普通商家
                        '//a[@class="dianpu_link"]/@href',
                        # 默认为 个人车
                    ),
                    'processors': ['58.source_type'],
                    # 'default': SOURCE_TYPE_GONGPINGJIA,
                },
                'is_certifield_car': {
                    # 默认不是，从同步时确认
                    'default': False,
                },
            },
        },
    }
}

fmt_rule_urls(rule)
# start_url = rule['start_urls'][0]
# if ('html' in start_url and len(start_url) > 40) \
#         or rule['parse']['url']['contains'][0] in start_url:
#     rule['parse'] = rule['parse_detail']