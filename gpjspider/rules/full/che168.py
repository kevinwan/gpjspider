# -*- coding: utf-8 -*-

from gpjspider.utils.constants import *
from .utils import *

_has = lambda x: has(x, '/..')

item_rule = {
    "class": "UsedCarItem",
    "fields": {
        'title': {
            'xpath': (
                text(cls('car-info', '/h2/a')),
                text(cls('car-h', '/h2/a')),
                text(cls('breadnav', '/a[4]')),
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
                #after_has(u'本车标签'),
            #),
            'default': '%(title)s',
        },
        'year': {
            'xpath': (
                attr(id_('car_firstregtime'), 'value'),
                text(cls('step-ul', '/li[2]')),
            ),
        },
        'month': {
            'xpath': (
                attr(id_('car_firstregtime'), 'value'),
                text(cls('step-ul', '/li[2]')),
            ),
        },
        'time': {
            'xpath': (
                text(cls('ml10')),
            ),
        },
        'mile': {
            #'xpath': (
                #has(u'行驶里程'),
            #),
            'default': '%(meta)s',
        },
        'volume': {
            'xpath': (
                has(u'发 动 机', '/span'),
            ),
            'default': '%(title)s',
        },
        'color': {
            'xpath': (
                '//title/text()',
            ),
            'processors': ['first', 'che168.color'],
        },
        'control': {
            'xpath': (
                has(u'变 速 器', '/span'),
                '//*[@class="h2-list"]/div[2]/text()[3]',
            ),
            'default': '%(title)s',
            'regex': u'([手自]{1,2}一?[动体])',
            'regex_fail': None,
        },
        'price': {
            'xpath': (
                text(id_('carbase_carprice')),
                text(id_('carprice')),
            ),
        },
        'price_bn': {
            'xpath': [
                attr(id_('car_specid'), 'value'),
                attr(id_('car_cid'), 'value'),
            ],
            'processors': ['che168.price_bn'],
        },
        'brand_slug': {
            'xpath': (
                #'//*[@class="breadnav"]/a[last()-1]/text()',
                text(cls('breadnav', '/a[last()-1]')),
            ),
            'regex': u'二手(.*)',
            'regex_fail': '',
        },
        'model_slug': {
            'xpath': (
                #has(u'车辆系列'),
                #'//*[@class="breadnav"]/a[last()]/text()',
                text(cls('breadnav', '/a[last()]')),
            ),
            'regex': u'二手(.*)',
            'regex_fail': '',
        },
        'model_url': {
            'xpath': (
                href(cls('breadnav', '/a[last()]')),
            ),
            'processors': ['first', 'che168.model_url'],
        },
        #'status': {
            #'xpath': (
                #has(u'车辆类型'),
            #),
            #'processors': ['first', 'cn2che.status'],
        #},
        'city': {
            'xpath': (
                '//title/text()',
            ),
            'processors': ['first', 'che168.city'],
        },
        'region': {
            'xpath': (
                text(id_('carOwnerInfo', '/div[2]')),
            ),
        },
        'phone': {
            'xpath': (
                has(u'咨询电话'),
                has(u'咨询电话', '/span'),
                attr(cls('phone-div', '/img'), 'src'),
            ),
            'processors': ['first', 'che168.phone'],
        },
        'contact': {
            'xpath': (
                text(id_('carOwnerInfo', '/div[1]/span[1]')),
            ),
        },
        'company_name': {
            'xpath': (
                text(cls('merchant-name', '/div/a')),
            ),
        },
        'company_url': {
            'xpath': (
                href(cls('merchant-name', '/div/a')),
            ),
            'format': True,
        },
        #'driving_license': {
            #'xpath': (
                #'//*[@id="other_infor1"]/div[1]/p/span[2]/text()',
            #),
        #},
        #'invoice': {
            #'xpath': (
                #'//*[@id="other_infor1"]/div[1]/p/span[4]/text()',
            #),
        #},
        #'maintenance_record': {
            #'xpath': (
                #has(u'保养情况', '/..'),
            #),
        #},
        'quality_service': {
            'xpath': (
                '//*[@id="base_carservice"]/ul/li//@title',         # 普通车
                after_has(u'服务承诺'),                             # 家家好车
                text(cls('last', '/h3')),                           # 家认证
            ),
            'processors': ['join'],
        },
        'description': {
            'xpath': (
                text(cls('p-tx')),                                  # 普通车
                '//*[@class="compile-tx"]//text()',                 # 家家好车
            ),
            'processors': ['join'],
        },
        'imgurls': {
            'xpath': (
                attr(cls('focusimg-pic', '/ul/li'), 'alt'),
                attr(cls('explain', '//img'), 'src2'),
            ),
            'processors': ['join'],
        },
        'mandatory_insurance': {
            'xpath': (
                has(u'保险还有', '/..'),
                has(u'保险已', '/..'),
                has(u'保险到期'),
            ),
        },
        #'business_insurance': {
            #'xpath': (
                #_has(u'商业险'),
            #),
        #},
        'examine_insurance': {
            'xpath': (
                #text(cls('step-ul', '/li[4]')),
                has(u'距离下一次年检时间', '/..'),              # 家认证、家家好车
                has(u'年检到期'),
            ),
        },
        'transfer_owner': {
            'xpath': (
                has(u'过户次数', '/span'),
            ),
        },
        'is_certifield_car': {
            'xpath': [
                text(cls('breadnav', '/a[1]')),             # 家家好车、家认证
                has(u'品牌认证'),
                has(u'保障车'),
                has(u'进入店铺'),
            ],
            'processors': ['che168.is_certifield_car'],
        },
        'source_type': {
            'xpath': [
                text(cls('breadnav', '/a[1]')),             # 家家好车、家认证
                has(u'品牌认证'),
                has(u'保障车'),
                has(u'进入店铺'),
            ],
            'default': SOURCE_TYPE_GONGPINGJIA,
            'processors': ['che168.source_type'],
        },
        'car_application': {
            'xpath': (
                after_has(u'原车用途'),
            ),
            'regex': u'(.*运)',
            'regex_fail': None,
        },
        #'condition_level': { # 原网站有 车况 的字段，但是都是 非常好，没什么用
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
    'url': {
        'xpath': (
            '//*[@class="all-source"]//div[@class="pic"]/a[@href]/@href',
            href(id_('carOwnerType', '/li/a')),
        ),
        'excluded': ['/autonomous/'],
        'format': True,
        'processors': ['clean_anchor'],
        'step': 'parse_detail',
        'update': True,
        'category': 'usedcar'
    },
    'next_page_url': {
        'xpath': (
            '//a[@class="page-item-next"]/@href',
            url(after('*[@id="carOwnerType"]//li[@class="current"]', '*')),
        ),
        'format': True,
        'processors': ['clean_anchor'],
        'step': 'parse',
    },
}


rule = {
    'name': u'二手车之家',
    'domain': 'che168.com',
    'base_url': 'http://www.che168.com',
    'spider': {
        'domain': 'che168.com',
        'download_delay': 2.5,
    },
    'start_urls': [
        'http://www.che168.com/china/a0_0msdgscncgpi1ltocspexp1e3/', # 首页、只看有图、时间倒排序
        #'http://www.che168.com/china/a0_0ms3dgscncgpi1lto8cspexp1e3/', # 认证车源
        #'http://www.che168.com/authentication/5028866.html', # 家认证
        #'http://hao.autohome.com.cn/5239567.html', # 家好车
        #'http://www.che168.com/dealer/109121/5036252.html', # 品牌认证
        #'http://www.che168.com/dealer/118132/5381345.html', # 保障车
        #'http://www.che168.com/dealer/131975/5381232.html', # 商家车源
        #'http://www.che168.com/personal/5381429.html', # 个人车源
    ],

    'parse': parse_rule,

    'parse_detail': {
        "item": item_rule,
    }
}

fmt_rule_urls(rule)
#rule['parse'] = rule['parse_detail']
