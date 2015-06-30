# -*- coding: utf-8 -*-
from .utils import *

item_rule = {
    'class': 'UsedCarItem',
    'fields': {
        'title': {
            'xpath': (
                text(cls('title', prefix=id_('basic') + '//')),
                attr(id_('car_info'), 'value'),
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
                after_has(u'上牌'),
            ),
            'default': '%(meta)s',
        },
        'month': {
            'xpath': (
                # u'//*[contains(text(), "\u4e0a\u724c")]/following-sibling::*/text()',
                after_has(u'上牌'),
            ),
            'default': '%(meta)s',
        },
        'mile': {
            'xpath': (
                # u'//*[contains(text(), "\u4eea\u8868\u76d8")]/following-sibling::*/text()',
                after_has(u'仪表盘'),
                u'//*[contains(text(), u"行驶里程") | contains(text(), u"万公里")]/text()',
            ),
        },
        'volume': {
            'default': '%(meta)s',
            'regex': u'排气量[^：]{,4}：([^;\\s]+)',
        },
        'color': {
            'xpath': (
                # u'//*[contains(text(), "\u989c\u8272")]/following-sibling::*/text()',
                after_has(u'颜色'),
            ),
        },
        'control': {
            'xpath': (
                # u'//*[contains(text(), "\u53d8\u901f\u7bb1")]/following-sibling::*/text()',
                after_has(u'变速箱'),
            ),
            'processors': ['last']
        },
        'price': {
            'xpath': (
                # '//*[@id="car_price"]/@value',
                attr(id_('car_price'), 'value'),
            ),
        },
        'price_bn': {
            'xpath': (
                '//*[@id="basic"]/div[2]/div/div/div[1]/ul[1]/li/text()',
                # '//*[@id="newCarPriceG"]/@value',
                attr(id_('newCarPriceG'), 'value'),
            ),
        },
        'brand_slug': {
            'default': '%(title)s',
            'before': ' ',
        },
        'model_slug': {
            'default': '%(title)s',
            'before': ' ',
        },
        'city_slug': {
        },
        'region': {
            'xpath': (
                # '//div[@class="text-block bottom-right"]/h3/text()',
                #text(cls('text-block bottom-right', '/h3')),
                #text(cls('text-block bottom-left', '/h3')),
                #u'//*[@id="gallery"]/div[1]/div[1]/div/div/div/div/h3/text()',  # 其它地方方式不能很好的工作
                text(id_('gallery', '/div[1]/div[1]/div/div/div/div/h3')),  # 其它地方方式不能很好的工作
            ),
            'processors': ['first', 'renrenche.region'],
        },
        'phone': {
            'default': '%(meta)s',
            'after': u'详询',
        },
        'company_name': {
            'default': u'人人车',
        },
        'company_url': {
            'default': 'http://www.renrenche.com/',
        },
        'driving_license': {
        },
        'invoice': {
            'xpath': (
                # u'//*[contains(text(), "\u8d2d\u8f66\u53d1\u7968")]/following-sibling::*/text()',
                after_has(u'购车发票'),
            ),
        },
        'maintenance_record': {
            'xpath': (
                # u'//*[contains(text(), "\u662f\u54264S\u5e97\u4fdd\u517b")]/following-sibling::*/text()',
                after_has(u'是否4S店保养'),
            ),
            # 'processors': ['has_maintenance_record']
        },
        'is_certifield_car': {
            'default': True,
        },
        'description': {
            'xpath': (
                # '//div[@class="main"]/div/p/text()',
                text(cls('main', '/div/p')),
            ),
        },
        'mandatory_insurance': {
            'xpath': (
                # u'//*[contains(text(), "\u4ea4\u5f3a\u9669")]/following-sibling::*/text()',
                after_has(u'交强险'),
            ),
        },
        'business_insurance': {
            'xpath': (
                after_has(u'商业险到期时间'),
                #u'//li/span[contains(text(), "商业险到期时间")]/../text()',
            ),
        },
        'imgurls': {
            'xpath': (
                # '//div[@class="container detail-gallery"]/div//img/@src',
                attr(cls('container detail-gallery', '/div//img'), 'src'),
                # '//div[@class="detail-box-bg"]/img/@src'
                attr(cls('detail-box-bg', '/img'), 'src'),
            ),
            'processors': ['join']
        },
        'quality_service': {
            'xpath': (
                u'//td[contains(text(), "\u670d\u52a1\u9879")]/following-sibling::td//td/text()[2]',
            ),
            'processors': ['join'],
        },
        'business_insurance': {
            'xpath': (
                # u'//*[contains(text(), "\u5546\u4e1a\u9669")]/following-sibling::*/text()',
                after_has(u'商业险'),
            ),
        },
        'source_type': {
            'default': 2,
        },
        'car_application': {
        },
        'city': {
            'xpath': (
                # u'//*[contains(text(), "\u5f52\u5c5e\u5730")]/following-sibling::*/text()',
                after_has(u'归属地'),
            ),
        },
        'dmodel': {
            'default': '%(title)s',
            # 'after': '-',
        },
        # 'condition_level': {
        #     'xpath': (
        #         # '//span[@class="desc"]/text()',
        #         text(cls('desc')),
        #     ),
        #     'processors': ['renrenche.cond_level'],
        # },
        'contact': {
            'xpath': (
                text(cls('owner-info', '/strong')),
            ),
            'default': u'人人车客服',
        },
        'examine_insurance': {
            'xpath': (
                # u'//*[contains(text(), "\u5e74\u68c0")]/following-sibling::*/text()',
                after_has(u'年检'),
            ),
        },
        'transfer_owner': {
            'xpath': (
                # u'//*[contains(text(), "\u8fc7\u6237\u6b21\u6570")]/following-sibling::*/text()',
                after_has(u'过户次数'),
            ),
        },
        # 'condition_detail': {
        #     'xpath': (
        #         # '//span[@class="desc"]/text()',
        #         text(cls('desc')),
        #     ),
        # },
        'time': {
            'xpath': (
                # u'//*[contains(text(), "\u68c0\u6d4b\u65f6\u95f4")]/text()',
                has(u'检测时间'),
                # u'//*[contains(text(), "\u53d1\u5e03\u65f6\u95f4")]/text()',
                has(u'发布时间'),
                #u'//*[contains(text(), "\u53d1\u5e03\u65f6\u95f4")]/following-sibling::*/text()',
                after_has(u'发布时间'),
            ),
            'processors': ['first', 'after_colon', 'gpjtime']
        },
    },
}

list_rule = {
    'url': {
        'xpath': ('//*[contains(@class,"list-item")]/a[@href]/@href',),
        'step': 'parse_detail',
        # 'contains': ['/cn/car'],
        # 'contains': '/cn/car',
        'format': True,
    },
    'next_page_url': {
        'xpath': ('//a[text()=">"]/@href',),
        'step': 'parse',
        'format': True,
        # 'incr_pageno': 3,
    }
}

rule = {
    'domain': 'renrenche.com',
    'name': u'人人车',
    'base_url': 'http://www.renrenche.com',
    'per_page': 40,
    'pages': 300,
    'start_urls': [
        'http://www.renrenche.com/cn/ershouche',
        # 'http://www.renrenche.com/cn/car/824a070287b5e14f',
        # 'http://www.renrenche.com/cn/car/2f50736befc53e8d',
        # 'http://www.renrenche.com/cn/car/882c5b51c6a00d6d',
    ],
    'parse': list_rule,
    'parse_detail': {
        'item': item_rule,
    },
}

fmt_rule_urls(rule)
# rule['parse'] = rule['parse_detail']