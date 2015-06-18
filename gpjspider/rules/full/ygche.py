# -*- coding: utf-8 -*-
from .utils import *
from gpjspider.utils.constants import SOURCE_TYPE_SELLER

item_rule = {
    "class": "UsedCarItem",
    "fields": {
        'title': {
            'xpath': (
                text(cls('title')),
            ),
            'required': True,
        },
        'dmodel': {
            'xpath': (
                has(u'车辆信息：', '/..'),
            ),
        },
        'meta': {
            'xpath': (
                '//meta[@name="description" or @name="Description"]/@content',
            ),
        },
        'year': {  # 年 YYYY 19/20** int
            'xpath': (
                has(u'首次上牌时间：', '/..'),
            ),
        },
        'month': {  # 月 m 1-12 int
            'xpath': (
                has(u'首次上牌时间：', '/..'),
            ),
        },
        'mile': {  # ？万公里
            'xpath': (
                has(u'表显里程：', '/span'),
            ),
        },
        'volume': {  # \d.\d 升(L/T)
            'xpath': (
                has(u'排量：', '/..'),
            ),
        },
        'color': {  # 颜色描述：红、蓝色、深内饰。。
            'xpath': (
                has(u'车辆信息：', '/..'),
            ),
            'processors':['ygche.color'],
        },
        'control': {  # 手动/自动/手自一体
            'xpath': (
                has(u'车辆信息：', '/..'),
            ),
            'processors':['ygche.control'],
        },
        'price': {  # 车主报价或车源的成交价
            'xpath': (
                text(id_('emprice')),
            ),
        },
        'price_bn': {  # 新车/厂商指导价，不含过户税之类的
            'xpath' : (
                text(cls('price-color-gray')),
            ),
            'processors': ['ygche.price_bn'],
        },
        'brand_slug': {  # 网站自己的品牌
            'xpath': (
                u'//meta[@name="Keywords"]/@content',
            ),
            'processors':['ygche.brand_slug'],
        },
        'model_slug': {  # 网站自己的车系
            'xpath': (
                u'//meta[@name="Keywords"]/@content',
            ),
            'processors':['ygche.model_slug'],
        },
        'city': {  # 车源归属地、所在城市
            'xpath': (
                has(u'车辆所在：', '/..'),
            ),
        },
        'contact': {  # 联系人
            'xpath': (
            ),
        },
        'region': {  # 看车地点
            'xpath': (
                attr(id_('aaddress'), 'data-address'),
            ),
        },
        'phone': {  # 联系电话
            'xpath': (
                text(id_('em400')),
            ),
        },
        #'company_name': {  # 商家名称
            #'xpath': (
            #),
        #},
        #'company_url': {  # 商家地址
            #'xpath': (
            #),
        #},
        # 行驶证、发票 有/无/齐全/..
        'driving_license': {
            'xpath': (
                #u'//*[contains(text(), "行驶本")]/following-sibling::*/@class',
                u'//*[contains(text(), "\u884c\u9a76\u672c")]/following-sibling::*/@class',
            ),
            'processors': ['ygche.driving_license']
        },
        'invoice': {
            'xpath': (
                #u'//*[contains(text(), "购车发票")]/following-sibling::*/@class',
                u'//*[contains(text(), "\u8d2d\u8f66\u53d1\u7968")]/following-sibling::*/@class',
            ),
            'processors': ['ygche.driving_license']
        },
        #'maintenance_record': {  # 车辆是否保养: 保养记录 -> True/False
            #'xpath': (
                #has(u'保养记录：', '/..'),
            #),
        #},
        'maintenance_desc': { # 车辆保养记录描述
            'xpath': (
                has(u'保养记录：', '/..'),
            ),
        },
        # (有|无|全程|部分)?4S保养、不?齐全、有保养..
        'condition_level': { # 车况等级 123 > ABC > 优良
            'xpath': (
                attr(cls('rate pr', '/a'), 'class'),
            ),
            'processors': ['ygche.condition_level'],
        },
        'condition_detail': { # 车况介绍/检测报告
            'xpath': (
                text(cls('explain')),
            ),
        },
        #'description': {  # 车源描述，酌情去掉无用信息
            #'xpath': (
                #text(with_cls('benchepeizhi', '/')),
            #),
        #},
        'imgurls': {
            'xpath': (
                attr(cls('lazy'), 'data-original'),
            ),
            'processors': ['join'],
        },
        # 交强险、商业险、年检 YYYY-MM-1，需处理过期/到期之类的情况
        #'mandatory_insurance': {
            #'xpath': (
                #has(u'交强险有效期：', '/..'),
            #),
            #'processors': ['ygche.mandatory_insurance'],
        #},
        # 'business_insurance': {
        #     'xpath': (
        #         u'//li/span[contains(text(), "商业险到期时间")]/../text()',
        #     ),
        # },
        'examine_insurance': {
            'xpath': (
                has(u'年审有效期：', '/..'),
            ),
        },
        'transfer_owner': {# 过户次数 int
            'xpath': (
                has(u'过户记录：', '/..'),
            ),
            'processors': ['ygche.transfer_owner'],
        },
        'car_application': {# 家用/非营运/..
            'xpath': (
                has(u'车辆用途：', '/..'),
            ),
        },
        'time': {  # 最真实的发布时间
            'xpath': (
                has(u'上架时间：', '/span'),
            ),
        },
        'quality_service': {  # 质保服务, tag:
            'xpath': (
            ),
            'default': u'此车享受45天或1800公里先行赔付承诺保障',
        },
        'is_certifield_car': {  # 是否优质车
            # 质保服务 -> 网站提供的类似区分 -> 网站平台所有的车源性质
            'xpath': (
            ),
            'default': True,
        },
        'source_type': {  # 来源类型
            # 1老爬虫 2优质车商 3品牌认证车商 4个人车源 5普通车商
            # 从入口爬取的所有类型要全部覆盖且能正确区分
            'default': SOURCE_TYPE_SELLER,
        },
    },
}

parse_rule = {
    "url": {  # 车源详情链接
        "xpath": (
            u'//a[@onclick="aclick()"]//@href',
        ),
        'format': 'http://www.ygche.com.cn{0}',
        "step": 'parse_detail',  # 下一步解析车源详情信息
    },
    "next_page_url": {  # 车源列表翻页
        "xpath": (
            '//a[@class="pl15 forbidden next"]/@href',
        ),
        'format': True,
        "step": 'parse',
        'max_pagenum': 120,  # 全量爬取的最大页数
        'incr_pageno': 8,  # 增量爬取的最大页数
    },
}

rule = {
    'name': u'阳光车网',
    'domain': 'ygche.com.cn',
    'base_url': 'http://www.ygche.com.cn',
    # TODO: update spider for support
    'spider': {
        'domain': 'ygche.com.cn',
        'download_delay': 2.5,
    },
    # 'update': True,

    'start_urls': [
        'http://www.ygche.com.cn/chengdu/list/',
        'http://www.ygche.com.cn/lanzhou/list/',
        'http://www.ygche.com.cn/wuhan/list/',
        'http://www.ygche.com.cn/haerbing/list/',
        'http://www.ygche.com.cn/suzhou/list/',
        'http://www.ygche.com.cn/zhongshan/list/',
        'http://www.ygche.com.cn/nanning/list/',
        'http://www.ygche.com.cn/nanjing/list/',
        'http://www.ygche.com.cn/xiamen/list/',
        'http://www.ygche.com.cn/changzhou/list/',
        #'http://www.ygche.com.cn/detail/cd1032596.html',
        #'http://www.ygche.com.cn/detail/cd1041162.html',
        #'http://www.ygche.com.cn/detail/cd1040994.html',
    ],

    'parse': parse_rule,

    'parse_detail': {
        "item": item_rule,
    }
}

fmt_rule_urls(rule)
#rule['parse'] = rule['parse_detail']
