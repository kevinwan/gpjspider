# -*- coding: utf-8 -*-
from .utils import *
from gpjspider.utils.constants import SOURCE_TYPE_SELLER

_has = lambda x: has(x, '/..')

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
            # 'xpath': (
            #     text(cls('info-ul', '/li[1]')),
            # ),
            'default': '%(title)s',
        },
        'meta': {
            'xpath': (
                '//meta[@name="description" or @name="Description"]/@content',
            ),
        },
        'year': {  # 年 YYYY 19/20** int
            'xpath': (
                has(u'首次上牌', '/span'),
            ),
        },
        'month': {  # 月 m 1-12 int
            'xpath': (
                has(u'首次上牌', '/span'),
            ),
        },
        'mile': {  # ？万公里
            'xpath': (
                _has(u'里程'),
                has(u'里程', '/span'),
            ),
        },
        'volume': {  # \d.\d 升(L/T)
            'xpath': (
                _has(u'排量'),
            ),
            'default': '%(title)s',
        },
        'color': {  # 颜色描述：红、蓝色、深内饰。。
            'xpath': (
                _has(u'车辆信息'),
            ),
            # 'default': '%(dmodel)s',
            'processors': ['first', 'ygche.color'],
            # 'processors': ['ygche.color'],
        },
        'control': {  # 手动/自动/手自一体
            'xpath': (
                after_has(u'变速器形式'),
                has(u'变', '/span'),
            ),
            #'default': '%(title)s',
        },
        'price': {  # 车主报价或车源的成交价
            'xpath': (
                text(id_('emprice')),
            ),
        },
        'price_bn': {  # 新车/厂商指导价，不含过户税之类的
            'xpath': (
                text(cls('price-color-gray')),
            ),
            'processors': ['first', 'ygche.price_bn'],
        },
        'brand_slug': {  # 网站自己的品牌
            'xpath': (
                text(cls('w1200 bread-Crumbs', '/a[contains(@href, "list/b")]')),
                text(cls('w1200 bread-Crumbs', '/a[2]')),
            ),
        },
        'model_slug': {  # 网站自己的车系
            'xpath': (
                text(cls('w1200 bread-Crumbs', '/a[contains(@href, "list/s")]')),
                text(cls('w1200 bread-Crumbs', '/a[3]')),
            ),
            # 'default': '%(brand_slug)s',
            'processors': ['add_temp'],
        },
        'model_url': {
            'xpath': (
                href(cls('w1200 bread-Crumbs', '/a[contains(@href, "list/s")]')),
                href(cls('w1200 bread-Crumbs', '/a[3]')),
            ),
            'format': True,
        },
        'city': {  # 车源归属地、所在城市
            'xpath': (
                _has(u'车辆所在'),
            ),
        },
        # 'contact': {  # 联系人
        #     'xpath': (
        #     ),
        # },
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
        'status': {
            'xpath': (
                # text(id_('btnseecar')),
                u'//a[@class="already-buy"]',
            ),
            'processors': ['first', 'ygche.status'],
            'default': 'Y',
        },
        # 'company_name': {  # 商家名称
        #     'xpath': (
        #     ),
        # },
        # 'company_url': {  # 商家地址
        #     'xpath': (
        #     ),
        # },
        # 行驶证、发票 有/无/齐全/..
        'driving_license': {
            'xpath': (
                u'//*[contains(text(), "行驶本")]/following-sibling::*/@class',
            ),
            'processors': ['first', 'ygche.has_or_not'],
        },
        'invoice': {
            'xpath': (
                u'//*[contains(text(), "购车发票")]/following-sibling::*/@class',
            ),
            'processors': ['first', 'ygche.has_or_not'],
        },
        # 'maintenance_record': {  # 车辆是否保养: 保养记录 -> True/False
        #     'xpath': (
        #     _has(u'保养记录：'),
        #     ),
        # },
        'maintenance_desc': {  # 车辆保养记录描述
            'xpath': (
                _has(u'保养记录'),
            ),
        },
        # (有|无|全程|部分)?4S保养、不?齐全、有保养..
        'condition_level': {  # 车况等级 123 > ABC > 优良
            'xpath': (
                attr(cls('rate pr', '/a'), 'class'),
            ),
            'processors': ['first', 'ygche.condition_level'],
        },
        'condition_detail': {  # 车况介绍/检测报告
            'xpath': (
                text(cls('explain')),
            ),
        },
        # 'description': {  # 车源描述，酌情去掉无用信息
        #     'xpath': (
        #     text(with_cls('benchepeizhi', '/')),
        #     ),
        # },
        'imgurls': {
            'xpath': (
                attr(cls('lazy'), 'data-original'),
            ),
            'processors': ['join'],
        },
        # 交强险、商业险、年检 YYYY-MM-1，需处理过期/到期之类的情况
        'mandatory_insurance': {
            'xpath': (
                _has(u'交强险'),
            ),
        },
        # 'business_insurance': {
        #     'xpath': (
        #         u'//li/span[contains(text(), "商业险到期时间")]/../text()',
        #     ),
        # },
        'examine_insurance': {
            'xpath': (
                _has(u'年审有效期'),
            ),
        },
        'transfer_owner': {  # 过户次数 int
            'xpath': (
                _has(u'过户记录'),
            ),
        },
        'car_application': {  # 家用/非营运/..
            'xpath': (
                _has(u'车辆用途'),
            ),
        },
        'time': {  # 最真实的发布时间
            'xpath': (
                has(u'上架时间', '/span'),
            ),
        },
        'quality_service': {  # 质保服务, tag:
            'xpath': (
                u'//*[contains(text(), "天赔付")]/parent::*/@title',
            ),
        },
        'is_certifield_car': {  # 是否优质车
            # 质保服务 -> 网站提供的类似区分 -> 网站平台所有的车源性质
            # 'xpath': (
            # ),
            'default': '%(quality_service)s',
            'default': True,
        },
        'source_type': {  # 来源类型
            # 1老爬虫 2优质车商 3品牌认证车商 4个人车源 5普通车商
            # 从入口爬取的所有类型要全部覆盖且能正确区分
            'default': SOURCE_TYPE_SELLER,
        },
    },
}

list_rule = {
    "url": {  # 车源详情链接
        "xpath": (
            attr(cls('carInfo', '/h3/a'), 'href'),
        ),
        'format': True,
        "step": 'parse_detail',  # 下一步解析车源详情信息
    },
    "next_page_url": {  # 车源列表翻页
        "xpath": (
            '//a[@class="pl15 forbidden next"]/@href',
        ),
        'format': True,
        "step": 'parse_list',
        # 'max_pagenum': 120,  # 全量爬取的最大页数
        # 'incr_pageno': 8,  # 增量爬取的最大页数
    },
}

rule = {
    'name': u'阳光车网',
    'domain': 'ygche.com.cn',
    'base_url': 'http://www.ygche.com.cn',
    'per_page': 20,
    'pages': 2000,
    # 'update': True,

    'start_urls': [
        'http://www.ygche.com.cn/city.html',
        # 'http://www.ygche.com.cn/detail/cd1047760.html',
        # 'http://www.ygche.com.cn/nanning/list/',
        # 'http://www.ygche.com.cn/detail/gz1047261.html',
        # 'http://www.ygche.com.cn/detail/wh1047696.html',
        # 'http://www.ygche.com.cn/detail/nj1048021.html',
        # 'http://www.ygche.com.cn/detail/nn1045013.html',
        # 'http://www.ygche.com.cn/detail/cd1032596.html',
        # 'http://www.ygche.com.cn/detail/cd1041162.html',
        # 'http://www.ygche.com.cn/detail/cd1040994.html',
        # 'http://www.ygche.com.cn/detail/zs1041021.html', # 变速器关键词多
        # 'http://www.ygche.com.cn/detail/sz1040382.html', # 无新车价、无排量
        # 'http://www.ygche.com.cn/detail/cd1042422.html', # 在售
        # 'http://www.ygche.com.cn/detail/cd1019953.html', # 已售
        #'http://www.ygche.com.cn/detail/cd1001107.html',
        #'http://www.ygche.com.cn/detail/nn1025954.html',
        # 'http://www.ygche.com.cn/detail/gz1044279.html', # 变速器
    ],

    'parse': {
        'url': {
            'xpath': (
                url(has_cls('select_city', '/')),
            ),
            'format': True,
            'format': 'http://www.ygche.com.cn{0}list/',
            # 'format': 'http://www.ygche.com.cn{0}list/68.html',
            'step': 'parse_list',
        },
    },

    'parse_list': list_rule,
    # 'parse': list_rule,

    'parse_detail': {
        'item': item_rule,
    }
}

fmt_rule_urls(rule)
# rule['parse'] = rule['parse_detail']
