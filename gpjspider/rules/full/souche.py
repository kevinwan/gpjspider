# -*- coding: utf-8 -*-
from gpjspider.utils.constants import SOURCE_TYPE_SELLER
from .utils import *

rule = {
    'name': u'大搜车',
    'domain': 'souche.com',
    'base_url': 'http://www.souche.com',
    'start_urls': [
        'http://www.souche.com',
        # 'http://www.souche.com/henan/list-pg4',
        #'http://www.souche.com/pages/choosecarpage/choose-car-detail.html?carId=82807b3d-58ee-4ec9-a126-1a9a6a1fe424',
        #'http://www.souche.com/pages/choosecarpage/choose-car-detail.html?carId=6qrVlpwIIY',
        # 'http://www.souche.com/pages/choosecarpage/choose-car-detail.html?carId=6NaYXhP2BW',
        # 'http://www.souche.com/pages/choosecarpage/choose-car-detail.html?carId=353aa97a-6559-48ab-b9e3-f4342a51778e',
    ],

    'parse': {
        "url": {
            "xpath": (
                '//div[@class="area-line"]/a/@data-pinyin',
            ),
            "format": "http://www.souche.com/{0}/list",
            # "format": "http://www.souche.com/{0}/list-mx2014-styishou",
            "step": 'parse_list',
            # 'default': ['http://www.souche.com/pages/choosecarpage/choose-car-detail.html?carId=6e4acb6b-7182-4e5a-97ff-2123138ea1d8'],
            # "step": 'parse_detail',
        }
    },
    'parse_list': {
        "url": {
            "xpath": (
                url(has_cls('carItem')),
            ),
            "format": True,
            "step": 'parse_detail',
        },
        "next_page_url": {
            "xpath": (
                '//a[@class="next"]/@href',
            ),
            "format": True,
            "step": 'parse_list',
            # 'max_pagenum': 10,
            # 'incr_pageno': 0,
        },
    },

    'parse_detail': {
        "item": {
            "class": "UsedCarItem",
            "fields": {
                'meta': {
                    'xpath': ('//meta[@name="Description"]/@content',),
                },
                'title': {
                    'xpath': (
                        '//div[@class="detail_main_info"]/div/h1/ins/text()',
                    ),
                    'required': True,
                },
                'dmodel': {
                    'default': '%(title)s',
                },
                'year': {
                    'xpath': (
                        '//div[@class="car_detail clearfix"]/div[1]/strong/text()',
                    ),
                },
                'month': {
                    'xpath': (
                        '//div[@class="car_detail clearfix"]/div[1]/strong/text()',
                    ),
                },
                'mile': {
                    # 'xpath': (
                    #     '//div[@class="car_detail clearfix"]/div[2]/strong/text()',
                    # ),
                    'default': '%(meta)s',
                },
                'volume': {
                    'xpath': (
                        u'//th[contains(text(), "排量")]/../td[not(@class)]/text()',
                    ),
                    'default': '%(title)s',
                },
                'color': {
                    'xpath': (
                        u'//th[contains(text(), "颜色")]/../td[not(@class)]/text()',
                    ),
                },
                'control': {
                    'xpath': (
                        u'//th[contains(text(), "变速箱")]/../td[not(@class)]/text()',
                    ),
                },
                'price': {
                    'xpath': (
                        '//div[@class="detail_price_left clearfix"]/em/text()',
                    ),
                },
                'price_bn': {
                    'xpath': ('//label[@class="new"]/text()',),
                },
                'brand_slug': {
                    'xpath': ('//div[@class="detail-map"]/a[last()-1]/text()',),
                },
                'model_slug': {
                    'xpath': ('//div[@class="detail-map"]/a[last()]/text()',),
                },
                'city': {
                    'xpath': (
                        '//div[@class="item"][3]/strong/text()',
                    ),
                },
                'description': {
                    'xpath': (
                        '//div[@class="sub_title"]/text()',
                    ),
                    'processors': ['join'],
                },
                'imgurls': {
                    'xpath': (
                        '//ul[@class="photosSmall"]/li/img/@data-original',
                    ),
                    'processors': ['join', 'souche.imgurls'],
                },
                'contact': {
                    'xpath': (
                        '//a[@class="shop-name"]/text()[1]',
                    ),
                },
                'phone': {
                    'xpath': (
                        '//div[@class="phone-num"]/text()',
                    ),
                },
                'company_name': {
                    'xpath': (
                        '//a[@class="shop-name"]/text()[1]',
                    ),
                },
                'company_url': {
                    'xpath': (
                        '//a[@class="shop-name"]/@href',
                    ),
                    'format': True,
                },
                'region': {
                    'xpath': (
                        text(cls('add')),
                    ),
                },
                # 'mandatory_insurance': {
                #     'xpath': (
                #         u'//td[contains(text(), "保险到期时间")]/following-sibling::td/text()',
                #     ),
                # },
                # 'examine_insurance': {
                #     'xpath': (
                #         u'//td[contains(text(), "年检有效期")]/following-sibling::td/text()',
                #     ),
                # },
                'time': {
                    'xpath': (
                        text(cls('push-time')),
                        has(u'质检时间'),
                    ),
                },
                'transfer_owner': {
                    'xpath': (
                        u'//p[@class="record-num"]/../table/tbody/tr',
                    ),
                    'processors': ['souche.transfer_owner'],
                    'default': 0,
                },
                'is_certifield_car': {
                    'default': '%(quality_service)s',
                },
                'source_type': {
                    'default': SOURCE_TYPE_SELLER,
                },
            },
        },
    },
}
fmt_rule_urls(rule)
#rule['parse'] = rule['parse_detail']