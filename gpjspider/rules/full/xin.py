# -*- coding: utf-8 -*-
"""
优信二手车 优质二手车 规则
"""
from gpjspider.utils.constants import SOURCE_TYPE_ODEALER
from .utils import *

item_rule = {
    "class": "UsedCarItem",
    "fields": {
        'title': {
            'xpath': (
                text(has_cls("tit", "/h1")),
            ),
            'required': True,
        },
        'dmodel': {
            'xpath': (
                text(cls('car-tit', '/p/a[5]')),
            ),
            'default': '%(title)s',
        },
        'meta': {
            'xpath': (
                '//meta[@name="description" or @name="Description"]/@content',
            ),
        },
        'year': {
            'xpath': (
                text(cls('br', u'/span[contains(text(), "上牌时间")]/following-sibling::em')),
                #u'//li[@class="br"]/span[contains(text(), "上牌时间")]/../em/text()',
            ),
        },
        'month': {
            'xpath': (
                text(cls('br', u'/span[contains(text(), "上牌时间")]/following-sibling::em')),
                #u'//li[@class="br"]/span[contains(text(), "上牌时间")]/../em/text()',
            ),
        },
        'mile': {
            'xpath': (
                text(cls('br', u'/span[contains(text(), "行驶里程")]/following-sibling::em')),
                u'//div[@class="info"]/ul/li[2]/em//text()',
                #u'//li[@class="br"]/span[contains(text(), "行驶里程")]/../em/text()',
            ),
        },
        'volume': {
            'xpath': (
                text(cls('br', u'/span[contains(text(), "排量")]/following-sibling::em')),
                #u'//li[@class="br"]/span[contains(text(), "排量")]/../em/text()',
            ),
            'default': '%(title)s',
        },
        'phone': {
            'xpath': (
                text(with_cls('tel', '//span')),
            ),
            'after': ' ',
        },
        'color': {
            'xpath': (
                after_has(u"颜色"),
                #u'//td[contains(text(), "颜色")]/following-sibling::td/text()',
            ),
        },
        'control': {
            'xpath': (
                after_has(u"变速箱"),
                #u'//td[contains(text(), "变速箱")]/following-sibling::td/text()',
            ),
            'default': '%(title)s',
        },
        'region': {
            'xpath': (
                text(cls("company", "/p[2]")),
            ),
        },
        'price': {
            'xpath': (
                text(cls("wan_1", "/em")),
            ),
        },
        'price_bn': {
            'xpath': (
                text(cls("wan_2", "/span/del")),
            ),
        },
        'brand_slug': {
            'xpath': (
                text(cls("tit", '/h1')),
            ),
        },
        'model_slug': {
            'xpath': [
                text(cls('car-tit', '/p/a[3]')),
                text(cls('car-tit', '/p/a[4]')),
                text(cls("tit", '/h1')),
            ],
            'processors': ['xin.model_slug']
        },
        'city': {
            'xpath': (
                has(u'销售城市', '/../em', 'li/span'),
                #u'//li/span[contains(text(), "销售城市")]/../em/text()',
            ),
        },
        'description': {
            'xpath': (
                text(cls('test-txt', '/ul/li')),
                #u'//div[@class="test-txt"]/ul/li/text()',
            ),
            'processors': ['join'],
        },
        'imgurls': {
            'xpath': (
                img(cls("carimg", "/div")),
                #'//div[@class="carimg"]/div/img/@src',
            ),
            'processors': ['join'],
        },
        'mandatory_insurance': {
            'xpath': (
                after_has(u'保险到期时间', 'td', 'td'),
                #u'//td[contains(text(), "保险到期时间")]/following-sibling::td/text()',
            ),
        },
        'company_name': {
            'xpath': (
                text(cls("newcompany", "/p")),
                #'//div[@class="newcompany"]/p/text()',
            ),
        },
        'company_url': {
            'xpath': (
                url(cls("newcompany")),
                #'//div[@class="newcompany"]/a/@href',
            ),
            'format': True,
        },
        'examine_insurance': {
            'xpath': (
                after_has(u'年检有效期'),
                #u'//td[contains(text(), "年检有效期")]/following-sibling::td/text()',
            ),
        },
        'transfer_owner': {
            'xpath': (
                after_has(u'过户次数'),
            ),
        },
        'car_application': {
            'xpath': (
                after_has(u'使用性质'),
            ),
        },
        'maintenance_desc': {
            'xpath': (
                after_has(u'保养情况'),
            ),
        },
        'quality_service': {
            'xpath': (
                u"//div[@class='day']/p/span[contains(text(), '退') or contains(text(), '修')  or \
                contains(text(), '换' or contains(text(), '保'))]/text()",
                u"//div[@id='msgMore']/div[@class='msg']/ul/li[contains(text(), '退') or contains(text(), '修') or \
                contains(text(), '换') or contains(text(), '保')]/text()",
                img(cls("test-txt", "/p")),
                img(cls('day-pic')),
            ),
            'processors': ['first', 'xin.quality_service']
        },
        'time': {
            'xpath': (
                after_has(u'检测时间', 'text()'),
            ),
        },
        'is_certifield_car': {
            # 'xpath': (
            #     exists(img(cls('day-pic'))),
            # ),
            'default': "%(quality_service)s",
            'default_fail': False,
            'processors': ['xin.is_certifield_car']
        },
        'source_type': {
            'xpath': (
                img(cls("test-txt", "/p")),
                img(cls('day-pic')),
            ),
            'default': SOURCE_TYPE_ODEALER,
            'processors': ['first', 'xin.source_type']
        },
    },
}

parse_rule = {
    "url": {
        "xpath": (
            url(has_cls('car-box', '//p')),
        ),
        "format": "http://www.xin.com{0}",
        'contains': '/c/',
        "step": 'parse_detail',
    },
    "next_page_url": {
        "xpath": (
            u'//a[contains(text(), "下一页")]/@data-page',
        ),
        "format": 'http://www.xin.com/quanguo/s/o2a10i{0}v1/',
        "step": 'parse',
    },
}

rule = {
    'name': u'优信二手车',
    'domain': 'xin.com',
    'start_urls': [
        'http://www.xin.com/quanguo/s/o2a10i1v1/',
        # 'http://www.xin.com/c/10353602.html',  # 2
        # 'http://www.xin.com/c/10254412.html',  # 3
        # 'http://www.xin.com/c/10354226.html',  # 5
        # 'http://www.xin.com/c/10354157.html',  # 2
        # 'http://www.xin.com/c/10358862.html',  # 3
        # 'http://www.xin.com/c/10376527.html',
    ],
    'base_url': 'http://www.xin.com',
    'per_page': 20,
    'pages': 12000,

    'parse': parse_rule,

    'parse_detail': {
        "item": item_rule,
    }
}

fmt_rule_urls(rule)
#rule['parse'] = rule['parse_detail']
