# -*- coding: utf-8 -*-
from gpjspider.utils.constants import SOURCE_TYPE_SELLER
from .utils import *

# _has = lambda x: has(x, '/..')
_has = after_has

item_rule = {
    "class": "UsedCarItem",
    "fields": {
        'title': {
            'xpath': (
                text(has_cls('car-particular-right', '/h2/a')),
            ),
            'required': True,
        },
        'meta': {
            'xpath': (
                '//meta[@name="description" or @name="Description"]/@content',
            ),
        },
        'year': {
            'xpath': (
                text(cls('date', '/ul/li[1]')),
            ),
        },
        'month': {
            'xpath': (
                text(cls('date', '/ul/li[1]')),
            ),
            #'default': '%(year)s',
        },
        'mile': {
            'xpath': (
                text(cls('date', '/ul/li[2]')),
            ),
        },
        'volume': {
            # 'xpath': (
            # ),
            'default': '%(title)s',
        },

        'color': {
            'xpath': (
                _has(u'车身颜色'),
            ),
        },
        'control': {
            'xpath': (
                after_has(u'变速器'),
                # text(id_('carDetailDiv', '/ul/li[2]')),
            ),
            'default': '%(title)s',
        },
        'price': {
            'xpath': (
                # text(cls('num', '/')),
                text(id_('priceNum')),
                text(cls('price', '/span[1]')),
            ),
            # 'processors': ['join'],
            'default': '%(meta)s',
        },
        'price_bn': {
            'xpath': (
                # text(cls('txt')),
                text(cls('price', '/span[2]')),
            ),
        },
        'brand_slug': {
            'xpath': (
                text('h2[@name="location"]/a[last()-1]'),
                after_has(u'品牌车系'),
                # text(id_('carDetailDiv', '/div[2]/ul[1]/li[4]')),
            ),
            'after': u'二手',
        },
        'model_slug': {
            'xpath': (
                text('h2[@name="location"]/a[last()]'),
                after_has(u'品牌车系'),
                # text(id_('carDetailDiv', '/div[2]/ul[1]/li[4]')),
            ),
            'after': u'二手',
        },
        'model_url': {
            'xpath': (
                href('h2[@name="location"]/a[last()]'),
            ),
            'format': True,
        },
        'city': {
            'xpath': (
                after_has(u'车辆所在地'),
                text('h2[@name="location"]/a[2]'),
            ),
        },
        'region': {
            'xpath': (
                text(cls('car-site')),
            ),
            'processors': ['last'],
        },
        'status': {
            'xpath': (
                '//' + has_cls('sold-out', '/a/text()'),
            ),
            'processors': ['first', '99haoche.status'],
        },
        'phone': {
            'xpath': (
                hidden('uploadid'),
            ),
            'processors': ['first', '99haoche.phone']
        },
        'company_name': {
            'xpath': (
                after_has(u'所属商家'),
            ),
        },
        'company_url': {
            'xpath': (
                after_has(u'所属商家', 'a/@href', get_text=False),
            ),
        },
        'driving_license': {
            'xpath': (
                _has(u'行驶证'),
            ),
        },
        'invoice': {
            'xpath': (
                _has(u'购车发票'),
            ),
        },
        'maintenance_record': {
            'xpath': (
                _has(u'保养记录'),
            ),
        },
        'quality_service': {
            'xpath': [
                has_attr2(u'质保承诺', 'title'),
                has_attr2(u'退换承诺', 'title'),
            ],
            'processors': ['join'],
        },
        'is_certifield_car': {
            'default': True,
        },
        'description': {
            'xpath': (
                text(has_cls('report-main', '/p[1]')),
                '//div[@class="postscript"]/p[1]/text()',
            ),
        },
        'imgurls': {
            'xpath': (
                attr(id_('img_R_L_List', '/li/a/img'), 'src'),
            ),
            'processors': ['join'],
        },
        'mandatory_insurance': {
            'xpath': (
                _has(u'交强险'),
            ),
        },
        'business_insurance': {
            'xpath': (
                _has(u'商业险'),
            ),
        },
        'examine_insurance': {
            'xpath': (
                after_has(u'年检有效期'),
            ),
        },
        'transfer_owner': {
            'xpath': (
                _has(u'是否一手车'),
            ),
        },
        'source_type': {
            'default': SOURCE_TYPE_SELLER,
        },
        'car_application': {
            'xpath': (
                _has(u'使用性质'),
            ),
        },
        'condition_level': {
            'xpath': (
                text(cls('rank-ico')),
                #构造链接请求服务器对应的 level 时，需要carid
                # hidden('uploadid'),
            ),
            # 'processors': ['99haoche.condition_level']
        },
    },
}

parse_rule = {
    "url": {
        "re": (
            r'http://www\.99haoche\.com/car/\d+\.html',
        ),
        "step": 'parse_detail',
    },
    "next_page_url": {
        "xpath": (
            '//a[@id="pagenow"]/following-sibling::a[1]/@href',
        ),
        'format': True,
        "step": 'parse',
        # 'incr_pageno': 3,
    },
}


rule = {
    'name': u'99好车',
    'domain': '99haoche.com',
    'start_urls': [
        'http://www.99haoche.com/quanguo/all/?p=v1',
        # 'http://www.99haoche.com/car/4496344.html',
        # 'http://www.99haoche.com/car/4486289.html',
        #'http://www.99haoche.com/car/4173771.html',
        #'http://www.99haoche.com/car/4483842.html',
        #'http://www.99haoche.com/car/4473155.html',
        # 'http://www.99haoche.com/car/4487656.html' # 已售
    ],
    'base_url': 'http://www.99haoche.com',
    # 'update': True,

    'parse': parse_rule,

    'parse_detail': {
        "item": item_rule,
    }
}

fmt_rule_urls(rule)
# rule['parse'] = rule['parse_detail']
