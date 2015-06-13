# -*- coding: utf-8 -*-
from gpjspider.utils.constants import SOURCE_TYPE_SELLER
from .utils import *

item_rule = {
    "class": "UsedCarItem",
    "fields": {
        'meta': {
            'xpath': ('//meta[@name="Description"]/@content',),
        },
        'title': {
            'xpath': (
                #'//div[@class="detail_main_info"]/div/h1/ins/text()',
                text(cls('detail_main_info', '/div/h1/ins')),
            ),
            'required': True,
        },
        'dmodel': {
            'default': '%(title)s',
        },
        'year': {
            'xpath': (
                #'//div[@class="car_detail clearfix"]/div[1]/strong/text()',
                text(cls('car_detail clearfix', '/div[1]/strong')),
            ),
        },
        'month': {
            'xpath': (
                #'//div[@class="car_detail clearfix"]/div[1]/strong/text()',
                text(cls('car_detail clearfix', '/div[1]/strong')),
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
                has(u"排量", '/../td[not(@class)]'),
                u'//th[contains(text(), "排量")]/../td[not(@class)]/text()',
            ),
            'default': '%(title)s',
        },
        'color': {
            'xpath': (
                #u'//th[contains(text(), "颜色")]/../td[not(@class)]/text()',
                has(u"颜色", '/../td[not(@class)]'),
            ),
        },
        'control': {
            'xpath': (
                #u'//th[contains(text(), "变速箱")]/../td[not(@class)]/text()',
                has(u"变速箱", '/../td[not(@class)]'),
            ),
        },
        'price': {
            'xpath': (
                #'//div[@class="detail_price_left clearfix"]/em/text()',
                text(cls('detail_price_left clearfix', '/em')),
            ),
        },
        'price_bn': {
            'xpath': (
                #'//label[@class="new"]/text()',
                text(cls('new')),
            ),
        },
        'brand_slug': {
            'xpath': (
                #'//div[@class="detail-map"]/a[last()-1]/text()',
                text(cls('detail-map', '/a[last()-1]')),
            ),
        },
        'model_slug': {
            'xpath': (
                #'//div[@class="detail-map"]/a[last()-1]/text()',
                text(cls('detail-map', '/a[last()]')),
            ),
        },
        'city': {
            'xpath': (
                #'//div[@class="item"][3]/strong/text()',
                text(cls('item', '[3]/strong')),
            ),
        },
        'description': {
            'xpath': (
                #'//div[@class="sub_title"]/text()',
                text(cls('sub_title')),
            ),
            'processors': ['join'],
        },
        'imgurls': {
            'xpath': (
                #'//ul[@class="photosSmall"]/li/img/@data-original',
                attr(cls('photosSmall', '/li/img/'), 'data-original'),
            ),
            'processors': ['join', 'souche.imgurls'],
        },
        'contact': {
            'xpath': (
                #'//a[@class="shop-name"]/text()[1]',
                #text(cls('shop-name')),
            ),
            #'processors': ['souche.second'],
            #'default': '%(company_name)s',
        },
        'phone': {
            'xpath': (
                #'//div[@class="phone-num"]/text()',
                text(cls('phone-num')),
            ),
        },
        'company_name': {
            'xpath': (
                '//a[@class="shop-name"]/text()[1]',
            ),
            #'default': '%(contact)s',
        },
        'company_url': {
            'xpath': (
                #'//a[@class="shop-name"]/@href',
                attr(cls('shop-name'), 'href'),
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
                #u'//p[@class="record-num"]/../table/tbody/tr',
                #cls('record-num', '/../table/tbody/tr'),
            ),
            'default': '%(url)s',
            'processors': ['souche.transfer_owner'],
        },
        'condition_level': {
            'xpath': (
                text(cls('zhijian type-item', '/div')),
            ),
            'processors': ['souche.condition_level'],
        },
        'quality_service': {
            'xpath': (
                text(cls('baoxian type-item', '/div')),
            ),
        },
        'is_certifield_car': {
            'default': '%(quality_service)s',
        },
        'source_type': {
            'default': SOURCE_TYPE_SELLER,
        },
    },
}

parse_rule = {
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
}

parse_list_rule = {
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
}

rule = {
    'name': u'大搜车',
    'domain': 'souche.com',
    'base_url': 'http://www.souche.com',
    'start_urls': [
        'http://www.souche.com',
        # 'http://www.souche.com/henan/list-pg4',
        # 'http://www.souche.com/pages/choosecarpage/choose-car-detail.html?carId=82807b3d-58ee-4ec9-a126-1a9a6a1fe424',
        # 'http://www.souche.com/pages/choosecarpage/choose-car-detail.html?carId=6qrVlpwIIY',
        # 'http://www.souche.com/pages/choosecarpage/choose-car-detail.html?carId=6NaYXhP2BW',
        # 'http://www.souche.com/pages/choosecarpage/choose-car-detail.html?carId=353aa97a-6559-48ab-b9e3-f4342a51778e',
        # 'http://www.souche.com/pages/choosecarpage/choose-car-detail.html?carId=73415fbf-31ff-42eb-8df1-b45b347ecfaa',
        # 'http://www.souche.com/pages/choosecarpage/choose-car-detail.html?carId=8dfddf7f-f4f6-45df-a62c-fd0420082b90',
    ],

    'parse': parse_rule,
    'parse_list': parse_list_rule,

    'parse_detail': {
        "item": item_rule,
    },
}
fmt_rule_urls(rule)
# rule['parse'] = rule['parse_detail']
