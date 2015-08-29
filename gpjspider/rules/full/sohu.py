# -*- coding: utf-8 -*-
from .utils import *
from gpjspider.utils.constants import *


def parse_meta(key, with_key=False):
    return with_key and u'(%s[^：]{,4}：[^;\s]+)' % key or u'%s[^：]{,4}：([^;\s]+)' % key

def get_url_and_source_type(response, spider):
    """
        主要是为了提取列表页的链接和对应的 source_type 信息，返回两部分的信息，
        一个是链接列表，一个是链接列表和对应的额外信息
        这里采用的方法是，一个 xpath 规则提取出来链接和是否认证车的信息，
        它们的关系是，如果一个链接对应的有认证车信息，那么在列表顺序上，就是认证信息紧跟着
        链接，如果没有，那么就是没有认证信息
    """
    xpath_rule = '//*[@class="carsItem carItem"]/a[@class="carImg"]/@href | //*[@class="car-price"]/*[@class="car-info-label"]/*[@class="info-item"]/text()'
    _urls = response.xpath(xpath_rule).extract()
    urls = set()
    meta_info = {}
    for idx, url in enumerate(_urls):
        if 'html' in url:
            urls.add(url)
        if u'认证' in url:
            meta_info[_urls[idx-1]] = dict(_source_type=url)
            break

    if meta_info:
        spider.log(u'{0} urls\' meta_info is: {1}'.format(len(urls), meta_info))
        # ipdb.set_trace()
    return urls, meta_info


item_rule = {
    'class': 'UsedCarItem',
    # 'debug': 'is_certifield_car',
    'fields': {
        'meta': {
            'xpath': (
                '//meta[@name="description" or @name="Description"]/@content',
            ),
        },
        'title': {
            'xpath': (
                text(cls('car-detail', '/h3')),
            ),
            'required': True,
        },
        'dmodel': {
            'default': '%(title)s',
            'after': '-',
        },
        'time': {
            'xpath': (
                has(u'发布时间'),
            ),
            'regex': u'发布时间：(.*)',
        },
        'is_certifield_car': {
            'default': '{item}',
            'processors': ['sohu.is_certifield_car'],
        },
        'source_type': {
            'default': '{item}',
            'processors': ['sohu.source_type'],
        },
        'city': {
            'default': '%(title)s',
            'before': '-',
        },
        'brand_slug': {
            'xpath': (
                '//meta[@name="keywords"]/@content',
            ),
            'processors': ['first', 'sohu.brand_slug'],
        },
        'model_slug': {
            'xpath': (
                '//meta[@name="keywords"]/@content',
            ),
            'processors': ['first', 'sohu.model_slug'],
        },
        'volume': {
            'xpath': (
                after_has(u'排量'),
            ),
        },
        'year': {
            'xpath': (
                after_has(u'上牌'),
            ),
        },
        'month': {
            'xpath': (
                after_has(u'上牌'),
            ),
        },
        'mile': {
            'xpath': (
                after_has(u'里程'),
            ),
        },
        'price_bn': {
            'xpath': (
                #has(u'新车'),
                text(cls('car-price-new')),
            ),
        },
        'price': {
            'xpath': (
                text(cls('car-price')),
            ),
        },
        'control': {
            'xpath': (
                after_has(u'变速器'),
            ),
        },
        #'transfer_owner': {
            #'xpath': (
                #after_has(u'是否一手车'),
                #u'//*[contains(text(), "过户次数")]/span/text()',
            #),
            #'processors': ['first', 'sohu.transfer_owner'],
        #},
        'color': {
            'xpath': (
                after_has(u'车辆颜色'),
            ),
        },
        #'mandatory_insurance': {
        #},
        #'business_insurance': {
            #'xpath': (
                #after_has(u'商业险'),
            #),
        #},
        #'examine_insurance': {
        #},
        #'car_application': {
        #},
        # condition_level
        # condition_detail
        # 'maintenance_record': {
        #     'xpath': (
        #         u'boolean(//*[contains(text(), "定期保养") or contains(text(), "定期4S保养")])',
        #         u'boolean(//*[contains(text(), "保养")])',
        #     ),
        #     'processors': ['first', 'has_maintenance_record'],
        # },
        #'maintenance_desc': {
            #'xpath': (
                #after_has(u'保养'),
                #u'//*[contains(text(), "保养")]/text()',
            #),
        #},
        'quality_service': {
            'xpath': (
                text(cls('service-span')),
            ),
            'processors': ['join'],
        },
        'driving_license': {
            'xpath': (
                after_has(u'行驶证'),
            ),
        },
        'invoice': {
            'xpath': (
                after_has(u'购车发票'),
                u'//*/span[contains(text(), "购车发票")]/../text()',
            ),
        },
        'imgurls': {
            'xpath': (
                attr(has_cls('img-nav', '//img'), 'big'),
            ),
            'processors': ['join'],
        },
        'company_name': {
            'xpath': (
                after_has(u'门店名称'),
            ),
            'processors': ['first', 'sohu.company_name'],
        },
        'company_url': {
            'xpath': (
                u'//*[contains(text(), "进入店铺")]/@href',
            ),
            'format': True,
        },
        'phone': {
            'xpath': (
                text(cls('car-contact-phone')),
            ),
        },
        'contact': {
            'xpath': (
                has(u'联系人'),
            ),
            'processors': ['first', 'after_colon'],
        },
        'region': {
            'xpath': (
                after_has(u'门店地址'),
            ),
            'processors': ['sohu.region'],
        },
        'status': {
            'xpath': (
                text(cls('car-contact fl bg_col')),
            ),
            'default': 'Y',
            'processors': ['first', 'sohu.status'],
        },
        'description': {
            'xpath': (
                after_has(u'车况介绍'),
            ),
        },

    },
}

parse_rule = {
    'url': {
        'xpath': {
            #'url': '//*[@class="carsItem carItem"]/a[@class="carImg"]/@href | //*[@class="car-price"]/*[@class="car-info-label"]/*[@class="info-item"]/text()',
            'function': get_url_and_source_type,
        },
        #'xpath_with_info': (
            #'//*[@class="carsItem carItem"]/a[@class="carImg"]/@href | //*[@class="car-price"]/*[@class="car-info-label"]/*[@class="info-item"]/text()',
        #),
        'format': True,
        'step': 'parse_detail',
        # 'match': '/buycar/carinfo',
        #'contains': ['/buycar/carinfo'],
        # 'excluded': ['/autonomous/'],
        #'processors': ['clean_anchor'],
    },
    'next_page_url': {
        'xpath': (
            '//*[@class="list-pager"]/a[last()]/@href',
            # url('div[@class="pager"]'),
            #url('*[@class="no"][last()]'),
            # '//div[@class="page"]/@href',
            # '//a[@class="page-item-next"]/@href',
            # '//a[@class="next_on"]/@href',
        ),
        'format': True,
        # 'max_pagenum': 150,  # 全量爬取的最大页数
        'incr_pageno': 6,
        # 'match': '/pg\d+.shtml',
        'step': 'parse',
    },
}

rule = {
    'name': u'搜狐二手车',
    'domain': '2sc.sohu.com',
    'base_url': 'http://2sc.sohu.com',
    'per_page': 15,
    'pages': 200,

    'start_urls': [
        'http://2sc.sohu.com/buycar/',
        'http://2sc.sohu.com/buycar/a0b0c0d0e0f0g3h0j0k0m0n0/',
        'http://2sc.sohu.com/buycar/a0b0c0d0e0f0g1h0j0k0m0n0/',
        'http://2sc.sohu.com/buycar/a0b0c0d0e0f0g2h0j0k0m0n0/',
        # 'http://2sc.sohu.com/buycar/a0b0c0d0e0f0g0h3j0k0m0n0/', # 全国二手车
        # 'http://2sc.sohu.com/buycar/a0b0c0d0e0f0g1h3j0k0m0n0/', # 个人车源
        # 'http://2sc.sohu.com/buycar/a0b0c0d0e0f0g2h3j0k0m0n0/', # 商家车源
        # 'http://2sc.sohu.com/buycar/a0b0c0d0e0f0g3h3j0k0m0n0/', # 认证车源
        # 'http://2sc.sohu.com/bj/buycar/carinfo_sohu_1548176.shtml',
        # 'http://2sc.sohu.com/fj-zhangzhou/buycar/carinfo_sohu_1521957.shtml',
        # 'http://2sc.sohu.com/buycar/a0b0c0d0e0f0g0h3j0k0m0n0/pg1.shtml',
        # 'http://2sc.sohu.com/buycar/a0b0c0d0e0f0g0h3j0k0m0n0s/',
        # Debug details
        # 'http://2sc.sohu.com/js-wuxi/buycar/carinfo_sohu_1508854.shtml',
        # 'http://2sc.sohu.com/bj/buycar/carinfo_sohu_1504198.shtml',
        # 'http://2sc.sohu.com/sh/buycar/carinfo_sohu_1510456.shtml',
        # 'http://2sc.sohu.com/bj/buycar/carinfo_sohuperson_1458746.shtml',
        # 'http://2sc.sohu.com/bj/buycar/carinfo_audi_1431865.shtml', # 3
        # 'http://2sc.sohu.com/zj-hz/buycar/carinfo_sohu_1485147.shtml', # 4
        # 'http://2sc.sohu.com/sc-cd/buycar/carinfo_sohu_1510419.shtml', # 5
        # 'http://2sc.sohu.com/bj/buycar/carinfo_sohu_1503731.shtml', # 5
        # 'http://2sc.sohu.com/sh/buycar/carinfo_sohu_1611825.shtml#品牌认证',
        #'http://2sc.sohu.com/nmg-hhht/buycar/carinfo_sohuperson_1610175.shtml', # 个人
        #'http://2sc.sohu.com/gd-foshan/buycar/carinfo_sohuperson_1620313.shtml',
        #'http://2sc.sohu.com/xj-wlmq/buycar/carinfo_sohuperson_1625324.shtml',
    ],

    'parse': parse_rule,
    'parse_detail': {
        'item': item_rule,
    },
}


fmt_rule_urls(rule)
#rule['parse'] = rule['parse_detail']
