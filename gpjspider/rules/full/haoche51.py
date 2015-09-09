# -*- coding: utf-8 -*-
from gpjspider.utils.constants import SOURCE_TYPE_SELLER
from .utils import *


def format_func(url_str):
    """
    javascript:window.open('http://bj.haoche51.com/details/20003.html')
    """
    s = url_str.find("javascript:window.open('")
    if s >= 0:
        s += len("javascript:window.open('")
    else:
        return None
    if not url_str.endswith("')"):
        return None
    else:
        return url_str[s:-2]


item_rule = {
    "class": "UsedCarItem",
    "fields": {
        'title': {
            'xpath': (
                text(cls("autotit", "//strong")),
                text(cls("autotit autotit-h3", "//strong")),
            ),
            'required': True,
        },
        'dmodel': {
            'default': '%(title)s',
        },
        'meta': {
            'xpath': (
                '//meta[@name="description" or @name="Description"]/@content',
            ),
        },
        'year': {
            'xpath': (
                text(cls("autotit", "/h2")),
                text(cls("autotit autotit-h3", "/h2")),
                #'//div[@class="autotit"]/h2/text()',
            ),
        },
        'month': {
            'xpath': (
                text(cls("autotit", "/h2")),
                text(cls("autotit autotit-h3", "/h2")),
                #'//div[@class="autotit"]/h2/text()',
            ),
        },
        'mile': {
            'xpath': (
                text(cls("autotit", "/h2")),
                text(cls("autotit autotit-h3", "/h2")),
                #'//div[@class="autotit"]/h2/text()',
            ),
        },
        'volume': {
            'xpath': (
                after_has(u'排量', 'li[1]'),
                #u'//li[contains(text(), "排量")]/following-sibling::li[1]/text()',
            ),
        },
        'control': {
            'xpath': (
                text(cls("autotit", "/h2")),
                text(cls("autotit autotit-h3", "/h2")),
                #'//div[@class="autotit"]/h2/text()',
            ),
            'processors': ['first', 'haoche51.control'],
        },
        'price': {
            'xpath': (
                text(cls("car-quotation", "/strong")),
                has(u"成交价", "/strong", 'div'),
                text(cls('prc-num')),
                #'//div[@class="car-quotation"]/strong/text()',
            ),
        },
        'price_bn': {
            'xpath': (
                after_has(u'厂商指导价', 'li[1]'),
            ),
            'regex': u'(.*)万元?',
        },
        'brand_slug': {
            'xpath': (
                text(cls("crumbs", "/a[3]")),
                text(cls("autotit", '/strong')),
                text(cls("autotit autotit-h3", '/strong')),
                #'//div[@class="autotit"]/strong/text()',
            ),
            'after': u'二手',
        },
        'model_slug': {
            'xpath': (
                text(cls("crumbs", "/a[4]")),
                text(cls("autotit", '/strong')),
                text(cls("autotit autotit-h3", '/strong')),
                #'//div[@class="autotit"]/strong/text()',
            ),
            # 'regex': u'.*二手(.*)'
            'after': u'二手',
        },
        'model_url': {
            'xpath': (
                href(cls("crumbs", "/a[4]")),
            ),
            # 'xpath': [
            #     href(cls("crumbs", "/a[1]")),
            #     href(cls("crumbs", "/a[4]")),
            # ],
            'format': True,
            # 'format': '%(url)s',
            # 'processors': ['concat'],
        },
        'city': {
            'xpath': (
                text(cls("crumbs", "/a[2]")),
                text(cls("crumbs", "/a[1]")),
                # '//div[@class="autotit"]/h2/text()',
            ),
            # 'regex': u'(.*?)好车无忧',
            # 'processors': ['first', 'haoche51.city'],
        },
        'region': {
            'xpath': (
                text(id_("kanche_addr")),
                # '//p[@class="own"]/text()',
            ),
            # 'processors': ['first', 'haoche51.region'],
        },
        'description': {
            'xpath': (
                text(cls("f-type03")),
                text(cls("ow-sa", "/p[not(@class)]")),
                has(u'评估师购车建议', '/..') + '|' + text(cls("said", '/p/')) + '|' + text(cls("tags", '/')),
                #'//p[@class="f-type03"]/text()',
                #'//div[@class="ow-sa"]/p[not(@class)]/text()'
            ),
            'processors': ['join'],
        },
        'imgurls': {
            'xpath': (
                '//ul[@class="mrd_ul"]/li/a/img/@data-original',
                '//div[@class="dtl-wrap scroll-anchor pmatrix"]/*/ul/li/img/@src',
                # '//div[@class="dt-pictype"]/img/@data-original',
            ),
            # 'processors': ['join', 'raw_imgurls'],
            'processors': ['join', 'strip_imgurls'],
        },
        'condition_detail': {
            'xpath': (
                # "//div[@class='cd-pc']/text()[4]",
                text(cls('ad-tit', '/')),
                "//div[@class='checker-text']/text()[2]",
            ),
            'processors': ['join'],
            'processors': ['concat'],
        },
        'contact': {
            'xpath': (
                '//p[@class="own"]/text()',
                after_has(u'车主说', 'div[@class="tdesc"]/text()'),
            ),
            'processors': ['first', 'haoche51.contact'],
            'before': u' • ',
        },
        'phone': {
            'xpath': (
                text(cls("tc-der", "/strong")),
                '//li[@class="tc-der"]/strong/text()',
                has(u'购车咨询', '/*[@class="tel-f00-18"]'),
            ),
        },
        'status': {
            'xpath': (
                u'//div[@class="car-has-deal"]',
                u'//div[@class="cnt-404"]//div[contains(text(),"页面不存在")]',
            ),
            'default': 'Y',
        },
        'mandatory_insurance': {
            'xpath': (
                has(u"交强险有效期", prefix="ul/li"),
                has(u"交强险有效期", prefix="tr/td"),
                has(u"交强险有效期", prefix="tr/tr"),
                # u'//div[@class="ow-sa1"]/ul/li[contains(text(), "交强")]/text()',
            ),
            'after': u'】',
        },
        'business_insurance': {
            'xpath': (
                has(u"商业险有效期", prefix="ul/li"),
                has(u"商业险有效期", prefix="td"),
                has(u"商业险有效期", prefix="tr"),
                # u'//div[@class="ow-sa1"]/ul/li[contains(text(), "商业")]/text()',
            ),
            'after': u'】',
        },
        'examine_insurance': {
            'xpath': (
                has(u"年检有效期", prefix="ul/li"),
                has(u"年检有效期", prefix="td"),
                has(u"年检有效期", prefix="tr"),
                # u'//div[@class="ow-sa1"]/ul/li[contains(text(), "年检")]/text()',
            ),
            'after': u'】',
        },
        'transfer_owner': {
            'xpath': (
                text(cls("autotit", "/h2")),
                text(cls("autotit autotit-h3", "/h2")),
                # text(cls("ow-sa", "/div[contains(text(), '过户次数')]/strong")),
            ),
            'processors': ['join', 'haoche51.transfer_owner'],
            # 'default': 1,
        },
        'quality_service': {
            'xpath': (
                text(cls('z-box', '/')),
                has(u"天可以退车",'/../','dd'),
                # text(cls('wyno')),
            ),
            'processors': ['join'],
        },
        'source_type': {
            'default': SOURCE_TYPE_SELLER,
            'default': SOURCE_TYPE_GONGPINGJIA,
        },
        'driving_license': {
            'xpath': (
                has(u"行驶证", prefix="li"),
                has(u"行驶证", prefix="td"),
                #u'//li[contains(text(), "行驶证")]/text()',
            ),
            # 'processors': ['first', 'haoche51.driving_license'],
            'processors': ['first', 'after_colon'],
            'after': u'】',
        },
        'invoice': {
            'xpath': (
                has(u"购车发票", prefix="li"),
                has(u"购车发票", prefix="td"),
                #u'//li[contains(text(), "购车发票")]/text()',
            ),
            # 'processors': ['first', 'haoche51.invoice'],
            'processors': ['first', 'after_colon'],
            'after': u'】',
        },
    },
}

list_rule = {
    "url": {
        "xpath": (
            attr(cls('car-products'), 'href'),
            # '//div[@class="content"]/div/div/@onclick',
        ),
        # "format": format_func,
        "step": 'parse_detail',
    },
    "next_page_url": {
        "xpath": (
            next_page(),
        ),
        "excluded": ("javascript:void()",),
        # "format": "http://haoche.ganji.com{0}",
        "step": 'parse_list',
        # "step": 'parse',
        'max_pagenum': 15,
        # 'max_pagenum': 80,
        'incr_pageno': 2,
    },
}

rule = {
    'name': u'好车无忧',
    'domain': 'haoche51.com',
    # 'base_url': '',
    # 'base_url': '%(url)s',
    'start_urls': [
        'http://bj.haoche51.com',
        # 'http://bj.haoche51.com/vehicle_list/p66.html',
        # 'http://cd.haoche51.com/vehicle_list/p80.html',
        # 'http://nj.haoche51.com/details/24703.html',
        # 'http://sh.haoche51.com/details/29401.html',
        # 'http://bj.haoche51.com/details/20936.html',
        # 'http://zz.haoche51.com/details/41917.html',
        # 'http://zz.haoche51.com/details/47736.html',  # phone is null
        # 'http://fs.haoche51.com/details/48179.html',  # title is null
        # 'http://fs.haoche51.com/details/46967.html',  # year is 0
    ],
    'per_page': 20,
    'pages': 250,

    'parse': {
        "url": {
            "xpath": (
                url(has_cls('city-cs')),
                # '//div[@id="layer_follow1"]/ul/li/div/a/@href',
            ),
            'format': '{0}vehicle_list.html',
            "step": 'parse_list',
        }
    },
    'parse_list': list_rule,
    # 'parse': list_rule,

    'parse_detail': {
        "item": item_rule
    },
}
# fmt_rule_urls(rule)

# rule['parse'] = rule['parse_detail']
