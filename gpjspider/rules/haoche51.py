# -*- coding: utf-8 -*-
"""
好车无忧优质二手车 规则

规则包含非 ascii 字符，必须使用 unicode 编码
"""
from gpjspider.utils.constants import SOURCE_TYPE_SELLER


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


rule = {
    #==========================================================================
    #  基本配置
    #==========================================================================
    'name': '优质二手车-好车无忧-规则',
    'domain': 'haoche51.com',
    'start_urls': ['http://bj.haoche51.com/vehicle_list.html'],

    #==========================================================================
    #  默认步骤  parse
    #==========================================================================
    'parse': {
        "url": {
            "xpath": ('//div[@id="layer_follow1"]/ul/li/div/a/@href',),
            "step": 'parse_list',
        }
    },
    #==========================================================================
    #  详情页步骤  parse_list
    #==========================================================================
    'parse_list': {
        "url": {
            "xpath": (
                '//div[@class="content"]/div/div/@onclick',
            ),
            "format": format_func,
            "step": 'parse_detail',
        },
        "next_page_url": {
            "xpath": (
                u'//a[contains(text(), "下一页")]/@href',
            ),
            "excluded": ("javscript",),
            # "format": "http://haoche.ganji.com{0}",
            # 新 url 对应的解析函数
            "step": 'parse_list',
        },
    },

    #==========================================================================
    #  详情页步骤  parse_detail
    #==========================================================================
    'parse_detail': {
        "item": {
            "class": "UsedCarItem",
            "fields": {
                'title': {
                    'xpath': ('//div[@class="autotit"]/strong/text()',),
                    'processors': ['first', 'strip'],
                    'required': True,
                },
                'meta': {
                    'xpath': (
                        '//meta[@name="Description"]/@content',
                        '//meta[@name="description"]/@content'
                    ),
                    'processors': ['first', 'strip'],
                },
                'year': {
                    'xpath': ('//div[@class="autotit"]/h2/text()',),
                    'processors': ['first', 'strip', 'haoche51.year'],
                },
                'month': {
                    'xpath': ('//div[@class="autotit"]/h2/text()',),
                    'processors': ['first', 'strip', 'haoche51.month'],
                },
                'mile': {
                    'xpath': ('//div[@class="autotit"]/h2/text()',),
                    'processors': ['first', 'strip', 'haoche51.mile'],
                },
                'volume': {
                    'xpath': (
                        u'//li[contains(text(), "排量")]/following-sibling::li[1]/text()',
                    ),
                    'processors': ['first', 'strip', 'gpjfloat'],
                },
                'control': {
                    'xpath': ('//div[@class="autotit"]/h2/text()',),
                    'processors': ['first', 'strip', 'haoche51.control'],
                },
                'price': {
                    'xpath': ('//div[@class="car-quotation"]/strong/text()',),
                    'processors': ['first', 'strip', 'gpjfloat'],
                },
                'price_bn': {
                    'xpath': ('//i[@class="newcarj"]/text()',),
                    'processors': ['first', 'strip', 'gpjfloat'],
                },
                'brand_slug': {
                    'xpath': ('//div[@class="autotit"]/strong/text()',),
                    'processors': ['first', 'strip', 'haoche51.brand_slug'],
                },
                'model_slug': {
                    'xpath': ('//div[@class="autotit"]/strong/text()',),
                    'processors': ['first', 'strip', 'haoche51.model_slug'],
                },
                'city': {
                    'xpath': ('//div[@class="autotit"]/h2/text()',),
                    'processors': ['first', 'strip', 'haoche51.city'],
                },
                'description': {
                    'xpath': (
                        '//p[@class="f-type03"]/text()',
                        '//div[@class="ow-sa"]/p[not(@class)]/text()'
                    ),
                    'processors': ['join', 'strip'],
                },
                'imgurls': {
                    'xpath': (
                        '//ul[@class="mrd_ul"]/li/a/img/@data-original',
                        '//div[@class="dt-pictype"]/img/@data-original',
                    ),
                    'processors': ['join', 'strip', 'strip_imgurls'],
                },
                'phone': {
                    'xpath': ('//li[@class="tc-der"]/strong/text()',),
                    'processors': ['join', 'strip'],
                },
                'mandatory_insurance': {
                    'xpath': (
                        u'//div[@class="ow-sa1"]/ul/li[contains(text(), "交强")]/text()',
                    ),
                    'processors': [
                        'first', 'strip', 'haoche51.mandatory_insurance'
                    ],
                },
                'business_insurance': {
                    'xpath': (
                        u'//div[@class="ow-sa1"]/ul/li[contains(text(), "商业")]/text()',
                    ),
                    'processors': [
                        'first', 'strip', 'haoche51.business_insurance'
                    ],
                },
                'examine_insurance': {
                    'xpath': (
                        u'//div[@class="ow-sa1"]/ul/li[contains(text(), "年检")]/text()',
                    ),
                    'processors': [
                        'first', 'strip', 'haoche51.examine_insurance'
                    ],
                },
                'transfer_owner': {
                    'xpath': (
                        # '//li[@class="guohu"]/text()',
                        '//div[@class="autotit"]/h2/text()[1]',
                        '//div[@class="ow-sa"]/div/strong/text()',
                    ),
                    'processors': ['first', 'strip', 'haoche51.transfer_owner'],
                    'default': 0,
                },
                'quality_service': {
                    'default': u' '.join([
                        u'只有高品质二手车',
                        u'完全杜绝事故车辆',
                        u'完全杜绝泡水车辆',
                        u'完全杜绝火烧车辆',
                        u'全程透明双方协商',
                        u'1年/2万公里放心质保',
                        u'14天可退车',
                    ])
                },
                'source_type': {
                    'default': SOURCE_TYPE_SELLER,
                },
                'driving_license': {
                    'xpath': (
                        u'//li[contains(text(), "行驶证")]/text()',
                    ),
                    'processors': ['first', 'strip', 'haoche51.driving_license'],
                },
                'invoice': {
                    'xpath': (
                        u'//li[contains(text(), "购车发票")]/text()',
                    ),
                    'processors': ['first', 'strip', 'haoche51.invoice'],
                },
            },
        },
    },
}
