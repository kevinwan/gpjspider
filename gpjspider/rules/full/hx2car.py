# -*- coding: utf-8 -*-
"""
华夏二手车
"""
from gpjspider.utils.constants import *
from .utils import *

_has = lambda x: has(x, '/..')

item_rule = {
    "class": "UsedCarItem",
    "fields": {
        'title': {
            'xpath': (
                text(cls('carname')),
            ),
            'required': True,
        },
        'meta': {
            'xpath': (
                '//meta[@name="description" or @name="Description"]/@content',
            ),
        },
        'dmodel': {
            #'xpath': (
                #text(cls('breadcrumb', '/a[5]/span')),
            #),
            'default': '%(title)s',
        },
        'year': {
            'xpath': (
                text(cls('carname')),
            ),
            'regex': u'(\d{4})年',
            'regex_fail': None,
        },
        'month': {
            'xpath': (
                text(cls('carname')),
            ),
            'regex': u'(\d{1,2})月',
        },
        'time': {
            'xpath': (
                has(u'更新时间'),
            ),
            'regex': u'更新时间：(.*)',
        },
        'mile': {
            'xpath': (
                has(u'里程', '/span'),
            ),
        },
        'volume': {
            'xpath': (
                after_has(u'排量'),
            ),
            'default': '%(title)s',
            'processors': ['first', 'hx2car.volume']
        },
        'color': {
            'xpath': (
                text(cls('carname')),
            ),
            'processors': ['hx2car.color'],
        },
        'control': {
            'xpath': (
                text(cls('carname')),
            ),
            'processors': ['hx2car.control'],
        },
        'price': {
            'xpath': (
                text(cls('carprice', '/span')),
                text(cls('jiage', '/span')),
            ),
        },
        'price_bn': {
            'xpath': (
                has(u'新车指导价'),
            ),
            'regex': u'(\d+\.?\d*)',
        },
        'brand_slug': {
            'xpath': (
                text(cls('glance_way', '/p/a[3]')),
            ),
        },
        'model_slug': {
            'xpath': (
                text(cls('glance_way', '/p/a[5]')),
            ),
            'regex': u'二手(.*)',
        },
        'model_url': {
            'xpath': (
                href(cls('glance_way', '/p/a[5]')),
            ),
            'format': True,
        },
        #'status': {
            #'xpath': (
                #attr(cls('details_one', '/strong/img'), 'src'),
            #),
            #'processors': ['first', 'xcar.status'],
            #'default': 'Q',
        #},
        'city': {
            'xpath': (
                text(cls('glance_way', '/p/a[5]')),
                text(cls('owner_area', '/span')),
            ),
            'processors': ['first', 'hx2car.city'],
            # 'regex': u'(.*?)二手',
        },
        'region': {
            'xpath': (
                after_has(u'联系地址'),
            ),
        },
        'status': {
            'xpath': (
                u'//*[contains(text(),"车辆已过期")]',
                # '//*[@class="error_zmb"]',
            ),
            'default': 'Y',
            'processors': ['first', 'hx2car.status'],
        },
        'phone': {
            'xpath': (
                text(cls('context_car')),
            ),
            'processors': ['hx2car.phone'],
        },
        'contact': {
            'xpath': (
                u'//*[@class="context_name"]/*[contains(text(), "联系人")]/following-sibling::*/em/text()',
                u'//*[@class="context_car"]/text()',
            ),
            'regex': u'[\u4e00-\u9fa5]+'
        },
        'company_name': {
            'xpath': (
                has(u'公司', '/span'),
            ),
        },
        'company_url': {
            'xpath': (
                u'//p[@class="owner_area"]/*[contains(text(), "网上门店")]/@href',
            ),
        },
        'driving_license': {
            'xpath': (
                '//*[@id="other_infor1"]/div[1]/p/span[2]/text()',
            ),
        },
        'invoice': {
            'xpath': (
                '//*[@id="other_infor1"]/div[1]/p/span[4]/text()',
            ),
        },
        #'maintenance_record': {
            #'xpath': (
                #_has(u'保养方式'),
            #),
        #},
        'quality_service': {
            'xpath': (
                has(u'已获担保'),
            ),
        },
        'description': {
            'xpath': (
                has(u'车辆描述', '/span'),
            ),
        },
        'imgurls': {
            'xpath': (
                attr(cls('detail_pic', '/img'), 'data-original'),
            ),
            'processors': ['join'],
        },
        'mandatory_insurance': {
            'xpath': (
                has(u'保险情况', '/span'),
            ),
        },
        #'business_insurance': {
            #'xpath': (
                #_has(u'商业险'),
            #),
        #},
        'examine_insurance': {
            'xpath': (
                has(u'年审情况', '/span'),
            ),
        },
        #'transfer_owner': {
            #'xpath': (
                #has(u'过户次数'),
            #),
            #'regex': u'过户次数：(.*)',
        #},
        'is_certifield_car': {
            #'xpath': (
                #has(u'认证车'),
            #),
            'default': 0,
        },
        'source_type': {
            'xpath': (
                has(u'公司', '/span'),
            ),
            'processors': ['first', 'hx2car.source_type'],
            'default': SOURCE_TYPE_GONGPINGJIA,
        },
        'car_application': {
            'xpath': (
                has(u'用途', '/span'),
            ),
        },
        #'condition_level': {
            #'xpath':(
            #),
        #},
        #'condition_detail': {
            #'xpath': (
                #has(u'准新车'),
            #),
        #},
    },
}

parse_rule = {
    "url": {
        'xpath': (
            attr(cls('listcar_title', '/a'), 'href'),
        ),
        'format': True,
        "step": 'parse_detail',
    },
    "next_page_url": {
        "xpath": (
            next_page(),
        ),
        'format': True,
        "step": 'parse',
        # 'incr_pageno': 3,
    },
}


parse_list = {
    'url': {
        're': (
            r'\w+/details/(\d+)',
        ),
        'format': 'http://hx2car.com/details/{0}',
        'step': 'parse_detail',
    },
    'next_page_url': {
        'xpath': (
            next_page(),
        ),
        'excluded': ['javascript'],
        'regex': 'currPage=(\d+)',
        'format': True,
        'format': '%(url)s',
        'replace': ['(currPage=\d+)', 'currPage={0}'],
        'step': 'parse_list',
        # 'dont_filter': False,
    },
}


rule = {
    'name': u'华夏二手车',
    'domain': 'hx2car.com',
    'base_url': 'http://hx2car.com',
    'dealer': {
        'url': '%scar.html?currPage=1',
    },
    'start_urls': [
        'http://hx2car.com/car/verify/f0000000ytdzsejckbmgl100000',
        'http://hx2car.com/car/essence/f0000000ytdzsejckbmgl100000',
        'http://hx2car.com/car/personal/f0000000ytdzsejckbmgl100000',
        'http://hx2car.com/car/stores/f0000000ytdzsejckbmgl100000',
        'http://hx2car.com/car/tradeallcar/f0000000ytdzsejckbmgl100000',
        #'http://hx2car.com/car/search.htm', # 列表首页、初审
        #'http://hx2car.com/details/143127330', # 个人二手车
        # 'http://hx2car.com/details/142977479', # 精品二手车
        #'http://hx2car.com/details/143030533', # 商家、精品
        #'http://hx2car.com/details/141568147', # 担保
        # 'http://beijing.hx2car.com/details/143803866'
        # 'http://hx2car.com/details/143779131' # pric,contact,quali,driv,invo
        # 'http://hx2car.com/details/143766257' # pric,conta,quali,driv,invo
        # 'http://hx2car.com/details/143687094'
        # 'http://hx2car.com/details/143837125' # volume
        # 'http://hx2car.com/details/143878702' # city
        # 'http://vip.hx2car.com/shxx/car.html?currPage=1',
    ],

    'parse': parse_rule,
    'parse_list': parse_list,
    'parse': parse_list,
    'parse_detail': {
        "item": item_rule,
    }
}

fmt_rule_urls(rule)
rule['parse'] = rule['parse_detail']
