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
        # 'http://www.souche.com/pages/choosecarpage/choose-car-detail.html?carId=6qrVlpwIIY',
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
            "format": "http://www.souche.com{0}",
            "step": 'parse_detail',
            'update': True,
            'category': 'usedcar'
        },
        "next_page_url": {
            "xpath": (
                '//a[@class="next"]/@href',
            ),
            "format": "http://www.souche.com{0}",
            "step": 'parse_list',
            # 'max_pagenum': 10,
            # 'incr_pageno': 0,
        },
    },

    'parse_detail': {
        "item": {
            "class": "UsedCarItem",
            'keys': [
                'meta', 'title', 'dmodel', 'city', 'city_slug', 'brand_slug', 'model_slug',
                'volume', 'year', 'month', 'mile', 'control', 'color', 'price_bn',
                'price', 'transfer_owner', 'car_application', 'mandatory_insurance', 'business_insurance', 'examine_insurance',
                'company_name', 'company_url', 'phone', 'contact', 'region', 'description', 'imgurls',
                'maintenance_record', 'maintenance_desc', 'quality_service', 'driving_license', 'invoice',
                'time', 'is_certifield_car', 'source_type',
            ],
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
                    'format': 'http://www.souche.com{0}',
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
                #  大搜车的准入规则决定都是 非运营
                'car_application': {
                    'default': u'非营运',
                },
                'quality_service': {
                    'default': u' '.join([
                        u'6年以内，12万公里以下 非营运车辆',
                        # u'七天包退、七天包修',
                        u'1年2万公里质保',
                    ])
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
# start_url = rule['start_urls'][0]
# if ('html' in start_url and len(start_url) > 40) \
#         or rule['parse']['url']['contains'][0] in start_url:
#     rule['parse'] = rule['parse_detail']