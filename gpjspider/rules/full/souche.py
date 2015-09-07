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
                text(cls('detail_main_info', '/div/h1/ins')),
            ),
            'required': True,
        },
        'dmodel': {
            'default': '%(title)s',
        },
        'year': {
            'xpath': (
                text(has_cls('car_detail', '/div[1]/strong')),
            ),
        },
        'month': {
            'xpath': (
                text(has_cls('car_detail', '/div[1]/strong')),
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
                # u'//th[contains(text(), "排量")]/../td[not(@class)]/text()',
            ),
            'default': '%(title)s',
        },
        'color': {
            'xpath': (
                has(u"颜色", '/../td[not(@class)]'),
            ),
        },
        'control': {
            'xpath': (
                has(u"变速箱", '/../td[not(@class)]'),
            ),
            'default': '%(title)s',
        },
        'price': {
            'xpath': (
                text(cls('detail_price_left clearfix', '/em')),
            ),
        },
        'price_bn': {
            'xpath': (
                text(cls('new')),
            ),
        },
        'brand_slug': {
            'xpath': (
                text(cls('detail-map', '/a[last()-1]')),
            ),
        },
        'model_slug': {
            'xpath': (
                text(cls('detail-map', '/a[last()]')),
            ),
            'processors': ['first', 'clean_space'],
        },
        'model_url': {
            'xpath': (
                href(cls('detail-map', '/a[last()]')),
            ),
            'format': True,
        },
        'city': {
            'xpath': (
                text(cls('item', '[3]/strong')),
            ),
        },
        'description': {
            'xpath': (
                text(cls('sub_title')),
            ),
            'processors': ['souche.strip_and_join'],
        },
        'imgurls': {
            'xpath': (
                attr(cls('photosSmall', '/li/img/'), 'data-original'),
            ),
            'processors': ['join', 'souche.imgurls'],
        },
        'status': {
            'xpath': (
                text(cls('detail-no')),
            ),
            'processors': ['first', 'souche.status'],
        },
        # 'contact': {
        #     'xpath': (
        #         text(cls('shop-name')),
        #     ),
        # },
        'phone': {
            'xpath': (
                text(cls('phone-num')),
            ),
        },
        'company_name': {
            'xpath': (
                '//a[@class="shop-name"]/text()[1]',
            ),
        },
        'company_url': {
            'xpath': (
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
                # has(u'质检时间'),
            ),
        },
        'transfer_owner': {
            'xpath': (
                # u'//p[@class="record-num"]/../table/tbody/tr',
                #cls('record-num', '/../table/tbody/tr'),
            ),
            'default': '%(url)s',
            'processors': ['souche.transfer_owner'],
        },
        'condition_level': {
            'xpath': (
                text(has_cls('zhijian', '/div')),
            ),
            'processors': ['souche.condition_level'],
        },
        'quality_service': {
            'xpath': (
                text(has_cls('baoxian', '/div')),
            ),
        },
        'is_certifield_car': {
            'default': True,
        },
        'source_type': {
            'default': SOURCE_TYPE_SELLER,
        },
    },
}

list_rule = {
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
        'incr_pageno': 2,
    },
}

rule = {
    'name': u'大搜车',
    'domain': 'souche.com',
    'base_url': 'http://www.souche.com',
    'start_urls': [
        'http://www.souche.com',
        # 'http://www.souche.com/henan/list-pg4',
        # 'http://www.souche.com/pages/choosecarpage/choose-car-detail.html?carId=ADoyq2JQbW',
        # 'http://www.souche.com/pages/choosecarpage/choose-car-detail.html?carId=f1441335-97a3-418f-abed-f5d9c1cedfaf',
        # 'http://www.souche.com/pages/choosecarpage/choose-car-detail.html?carId=1e7072d8-c8fc-422c-bcbc-2b0dd011ade4',
        # 'http://www.souche.com/pages/choosecarpage/choose-car-detail.html?carId=82807b3d-58ee-4ec9-a126-1a9a6a1fe424',
        # 'http://www.souche.com/pages/choosecarpage/choose-car-detail.html?carId=6qrVlpwIIY',
        # 'http://www.souche.com/pages/choosecarpage/choose-car-detail.html?carId=6NaYXhP2BW',
        # 'http://www.souche.com/pages/choosecarpage/choose-car-detail.html?carId=353aa97a-6559-48ab-b9e3-f4342a51778e',
        # 'http://www.souche.com/pages/choosecarpage/choose-car-detail.html?carId=73415fbf-31ff-42eb-8df1-b45b347ecfaa',
        # 'http://www.souche.com/pages/choosecarpage/choose-car-detail.html?carId=8dfddf7f-f4f6-45df-a62c-fd0420082b90',
        # 'http://www.souche.com/pages/choosecarpage/choose-car-detail.html?carId=353aa97a-6559-48ab-b9e3-f4342a51778e',
        # 'http://www.souche.com/pages/choosecarpage/choose-car-detail.html?carId=c41007ab-baf9-4c06-a787-c71bf48b463a',
        # 'http://www.souche.com/pages/choosecarpage/choose-car-detail.html?carId=2f38de4f-d180-498a-8092-8a977bde9f51',
    ],
    'per_page': 24,
    'pages': 200,

    'parse': {
        "url": {
            "xpath": (
                '//div[@class="area-line"]/a/@data-pinyin',
            ),
            "format": "http://www.souche.com/{0}/list",
            # "format": "http://www.souche.com/{0}/list-pg4",
            # "format": "http://www.souche.com/{0}/list-mx2014-styishou",
            "step": 'parse_list',
            # 'default': ['http://www.souche.com/pages/choosecarpage/choose-car-detail.html?carId=6e4acb6b-7182-4e5a-97ff-2123138ea1d8'],
            # "step": 'parse_detail',
        }
    },
    'parse_list': list_rule,
    # 'parse': list_rule,

    'parse_detail': {
        "item": item_rule,
    },
}
fmt_rule_urls(rule)
# rule['parse'] = rule['parse_detail']
