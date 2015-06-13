# -*- coding: utf-8 -*-
from .utils import *

item_rule = {
    "class": "UsedCarItem",
    "fields": {
        'title': {
            'xpath': (
                text(cls('h1')),
            ),
            'required': True,
        },
        'dmodel': {
            'default': '%(title)s',
            'regex': u'(\S+\d{2,4}款.+)\s\d{4}年上牌',
            'before': '[',
        },
        'meta': {
            'xpath': (
                '//meta[@name="description" or @name="Description"]/@content',
            ),
        },
        'year': {
            'xpath': (
                after_has(u'上牌时间'),
            ),
        },
        'month': {
            'xpath': (
                after_has(u'上牌时间'),
            ),
        },
        'mile': {
            'xpath': (
                after_has(u'行驶里程'),
            ),
        },
        'volume': {
            'xpath': (
                after_has(u'排量'),
            ),
        },
        'color': {
            'xpath': (
                after_has(u'颜色'),
            ),
        },
        'control': {
            # 'xpath': (
            #     after_has(u'变速箱'),
            # ),
            'default': '%(description)s %(dmodel)s',
            'default': '%(dmodel)s',
            'regex': u'变速箱：(\S+)| ([手自]\S+)',
            'regex': [u'变速箱：(\S+)', '\s?([手自]\S+)'],
            'regex': u' ([手自]\S*[动体])',
            # 'regex': u' [手自]\S+',
            'regex_fail': None,
            'regex_not': None,
            # 'processors': ['concat'],
        },
        'price': {
            'xpath': (
                text(cls('font_jiage')),
            ),
        },
        'price_bn': {
            'default': '%(description)s',
        },
        'brand_slug': {
            'xpath': (
                text(id_('carbrands')),
            ),
        },
        'model_slug': {
            'xpath': (
                text(id_('carseriess')),
            ),
        },
        'city': {
            'xpath': (
                '//meta[@name="location"]/@content',
            ),
            'processors': ['first', '58.city'],
        },
        'contact': {
            'xpath': (
                after_has(u'联系', 'span[1]//text()'),
            ),
        },
        'region': {
            'xpath': (
                text(id_('address_detail')),
            ),
        },
        'phone': {
            'xpath': (
                text(id_('t_phone', '/')),
            ),
            'processors': ['join'],
            'processors': ['concat'],
        },
        'company_name': {
            'xpath': (
                text(cls('font_yccp')),
            ),
        },
        'company_url': {
            'xpath': (
                url(cls('dianpu_link')),
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
                after_has(u'保养'),
            ),
        },
        'quality_service': {
            'xpath': (
                # text(id_('baozhang', '/')),
                text(cls('paddright13')),
                # has(u'质保'),
                # has(u'延保'),
            ),
            'processors': ['join'],
        },
        'description': {
            'xpath': (
                text(with_cls('benchepeizhi', '/')),
            ),
            'processors': ['join'],
            'before': u'温馨提示：',
        },
        'imgurls': {
            'xpath': (
                # img(id_('img1div')),
                attr(cls('mb_4'), 'src'),
            ),
            'processors': ['join'],
        },
        'mandatory_insurance': {
            'xpath': (
                after_has(u'交强'),
            ),
        },
        # 'business_insurance': {
        #     'xpath': (
        #         u'//li/span[contains(text(), "商业险到期时间")]/../text()',
        #     ),
        # },
        'examine_insurance': {
            'xpath': (
                after_has(u'年检'),
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
        'time': {
            'xpath': (
                text(cls('time')),
            ),
        },
        'source_type': {
            'xpath': [
                # 厂商认证
                # 'boolean(//div[@class="rz_biaozhi"])',
                exists(cls('rz_biaozhi')),
                # exists(id_('changshangrenzheng')),
                # 优质商家
                attr(has_id('icon_'), 'id'),
                # id_('icon_chengxincheshang'),
                # text(cls('paddright13')),
                # 普通商家
                url(cls('dianpu_link')),
                # '%(company_url)s',
                # 默认为 个人车
            ],
            # 'default': '%(company_url)s %(quality_service)s %(description)s',
            # 'default': '%(description)s %(quality_service)s %(company_url)s '.split(),
            'processors': ['58.source_type'],
        },
        'is_certifield_car': {
            'xpath': (
                # attr(has_id('icon_'), 'id'),
                # text(cls('paddright13')),
                exists(has_id('icon_')),
            ),
            'default': False,
            # 'default': '%(quality_service)s %(description)s',
            'default': '%(quality_service)s',
            'default_fail': None,
            # 'processors': ['join', '58.is_certifield_car'],
        },
    },
}

parse_rule = {
    "url": {
        'xpath': (
            url('*[@id="infolist"]//*[@sortid]/'),
        ),
        'contains': ['/ershouche/'],
        "step": 'parse_detail',
    },
    "next_page_url": {
        "xpath": (
            # url(cls('list-tabs')),
            '//a[@class="next"]/@href',
        ),
        'format': True,
        "step": 'parse',
        'max_pagenum': 25,
        'incr_pageno': 5,
        'incr_pageno': 8,
    },
}

rule = {
    'name': u'58同城',
    'domain': '58.com',
    'base_url': 'http://quanguo.58.com',
    # TODO: update spider for support
    'spider': {
        'domain': '58.com',
        'download_delay': 2.5,
    },
    # 'update': True,

    'start_urls': [
        'http://quanguo.58.com/ershouche/',
        'http://quanguo.58.com/ershouche/0/',
        'http://quanguo.58.com/ershouche/1/',
        'http://quanguo.58.com/ershouche/?xbsx=1',
        # 'http://quanguo.58.com/ershouche/pn15/',
        # 'http://quanguo.58.com/ershouche/0/pn15/',
        # 'http://quanguo.58.com/ershouche/1/pn15/',
        # 'http://quanguo.58.com/ershouche/pn15/?xbsx=1',
        # 'http://bj.58.com/ershouche/21942816658953x.shtml', # 2
        # 'http://bj.58.com/ershouche/22095630730144x.shtml', # 2
        # 'http://bj.58.com/ershouche/19417891266819x.shtml', # 2
        # 'http://sh.58.com/ershouche/21667174258462x.shtml', # 3
        # 'http://sy.58.com/ershouche/21851847601184x.shtml', # 4
    ],

    'parse': parse_rule,

    'parse_detail': {
        "item": item_rule,
    }
}

fmt_rule_urls(rule)
#rule['parse'] = rule['parse_detail']
