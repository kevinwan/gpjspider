# -*- coding: utf-8 -*-
from .utils import *
from gpjspider.utils.constants import *

_has = lambda x: has(x, '/..')

item_rule = {
    "class": "UsedCarItem",
    "fields": {
        'title': {
            'xpath': (
                text(has_cls("viewad-title")),
            ),
            'required': True,
        },
        'dmodel': {
            'xpath': (
                _has(u'车型'),
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
                _has(u'上牌年份'),
            ),
        },
        'month': {
            'xpath': (
                _has(u'上牌年份'),
            ),
        },
        'mile': {
            'xpath': (
                _has(u'行驶里程'),
            ),
        },
        'volume': {
            'xpath': (
                _has(u'排量：'),
            ),
            'default': '%(dmodel)s',
        },
        'phone': {
            'xpath': [
                text(id_('num')),
                '//a[@data-contact]/@data-contact',
            ],
            'processors': ['baixing.phone'],
        },
        'color': {
            'xpath': (
                _has(u'车辆颜色'),
            ),
            'processors': ['first', 'baixing.color'],
        },
        'control': {
            'xpath': (
                _has(u'变速箱'),
            ),
            'default': '%(dmodel)s',
            'regex': u'([手自]{1,2}一?[动体])',
            'regex_fail': None,
        },
        'region': {
            'xpath': (
                attr(id_('view-map'), 'href'),
                after_has(u'地区'),
            ),
            'processors': ['first', 'baixing.region'],
        },
        'price': {
            'xpath': (
                has(u'价格', '/strong'),
            ),
            'regex': '(\d+\.?\d{1,2})0*',
        },
        'brand_slug': {
            'xpath': (
                after_has(u'品牌：'),
            ),
        },
        'model_slug': {
            'xpath': [
                after_has(u'品牌：'),
                after_has(u'车系列：'),
            ],
            'processors': ['baixing.model_slug'],
            'default': '%(dmodel)s',
        },
        'model_url': {
            'xpath': (
                href(cls('head-nav head-bread', '/small[5]/a')),
            ),
            'format': True,
        },
        'city': {
            'xpath': (
                '//meta[@name="location"]/@content',
            ),
            'regex': u'city=(.*)',
        },
        'description': {
            'xpath': (
                '//meta[@name="description"]/@content',
            ),
        },
        'imgurls': {
            'xpath': (
                attr(cls('img sep', '/div/img'), 'src'),
            ),
            'processors': ['join'],
        },
        'mandatory_insurance': {
            'xpath': (
                _has(u'交强险到期'),
            ),
        },
        'company_name': {
            'xpath': (
                text(cls("shop-topic", '/a')),
            ),
        },
        'company_url': {
            'xpath': (
                url(cls("shop-topic")),
            ),
        },
        'examine_insurance': {
            'xpath': (
                _has(u'年检到期'),
            ),
        },
        'business_insurance': {
            'xpath': (
                _has(u'商业险到期'),
            ),
        },
        # 'transfer_owner': {
        #     'xpath': (
        #         after_has(u'过户次数'),
        #     ),
        # },
        'car_application': {
            'xpath': (
                _has(u'车辆用途'),
            ),
            'processors': ['first', 'baixing.car_application'],
        },
        # 'maintenance_desc': {
        #     'xpath': (
        #     ),
        # },
        # 'quality_service': {
        #     'xpath': (
        #     ),
        # },
        'invoice': {
            'xpath': (
                _has(u'购车发票'),
            ),
            'processors': ['first', 'baixing.invoice'],
        },
        'time': {
            'xpath': (
                u'//span[contains(@title, "首次发布于")]/@title',
            ),
            'regex': u'：(.*)',
        },
        'is_certifield_car': {
            'default': False
        },
        'source_type': {
             'xpath': (
                 text(cls("shop-topic", '/a')),
             ),
            'default': SOURCE_TYPE_GONGPINGJIA,
            'processors': ['first', 'baixing.source_type'],
        },
    },
}

parse_rule = {
    'url': {
        'xpath': (
            '//li[@data-aid]/a/@href',
        ),
        'contains': '/ershouqiche/',
        'processors': ['clean_param'],
        'step': 'parse_detail',
    },
    'next_page_url': {
        'xpath': (
            u'//a[contains(text(), "下一页")]/@href',
            href(has_cls('tab-title', '//a')),
            href(id_('tags', '//a')),
        ),
        'format': True,
        'format': {
            '/': True,
            '/': '%(url)s',
            'http': '{0}ershouqiche/?todayOnly=1',
        },
        'step': 'parse',
    },
}

rule = {
    'name': u'百姓二手车',
    'domain': 'baixing.com',
    'base_url': 'http://china.baixing.com',
    'base_url': '%(url)s',
    'start_urls': [
        # 'http://dongguan.baixing.com/ershouqiche/a820742742.html',
        # 'http://dongguan.baixing.com/ershouqiche/a785687239.html',
        'http://www.baixing.com/?changeLocation=yes',
        'http://china.baixing.com/ershouqiche/?todayOnly=1',
        'http://china.baixing.com/ershouqiche/?todayOnly=1&cheshang=1', # 品牌车商
        'http://china.baixing.com/ershouqiche/koala_1/?todayOnly=1', # 考拉二手车
        'http://china.baixing.com/ershouqiche/?imageFlag=1&page=8',
        # 'http://shanghai.baixing.com/ershouqiche/a749685037.html',
        # 'http://nanning.baixing.com/ershouqiche/a751473084.html',
        # 'http://dalian.baixing.com/ershouqiche/a761320262.html',
        # 'http://maoming.baixing.com/ershouqiche/a709950299.html',
        # 'http://chaoyang.baixing.com/ershouqiche/a745332976.html',
        # 'http://tianjin.baixing.com/ershouqiche/a738758222.html',
        # 'http://chaoyang.baixing.com/ershouqiche/a753358633.html',
        #'http://hangzhou.baixing.com/ershouqiche/a752358447.html', # 有行驶里程、上牌年份、品牌、车型
        #'http://chenzhou.baixing.com/ershouqiche/a605492920.html', # 排量、变速箱、车辆用途、行驶证、交强险、年检
        #'http://xian.baixing.com/ershouqiche/a634046170.html',
        #'http://nanning.baixing.com/ershouqiche/a765382531.html',
        #'http://qiandongnan.baixing.com/ershouqiche/a770089764.html', # 里程、价格是错误的
        #'http://shangqiu.baixing.com/ershouqiche/a781066618.html', # 有地图、地区
        #'http://tongling.baixing.com/ershouqiche/a781067063.html', # 无地图、地区
        #'http://tongling.baixing.com/ershouqiche/a704844017.html', # 有 model_url
        #'http://yantai.baixing.com/ershouqiche/a781067189.html', # control, volume
        #'http://quanzhou.baixing.com/ershouqiche/a776601726.html', # volume
        #'http://ningbo.baixing.com/ershouqiche/a788142311.html',
        #'http://yiyang.baixing.com/ershouqiche/a788264768.html', # 6.2800万元
    ],
    'per_page': 100,
    'pages': 100,
    # 'update': True,

    'parse': parse_rule,
    'parse_detail': {
        "item": item_rule,
    }
}

fmt_rule_urls(rule)
# rule['parse'] = rule['parse_detail']
