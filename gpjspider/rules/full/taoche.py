# -*- coding: utf-8 -*-
from .utils import *
import time

item_rule = {
    'class': 'UsedCarItem',
    'fields': {
        'title': {
            'xpath': (
                text(cls('tc14-cyxq-tit', '/h3')),
            ),
            'processors': ['join'],
            'after': ' - ',
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
        'time': {
            'xpath': (
                text(
                    cls('tc14-tabtitbox tc14-tab-h53  tc14-cytab clearfix', '/span')),
            ),
            'regex': '(\d{2,4}-\d{1,2}-\d{1,2})',
            'regex_fail': time.strftime('%Y-%m-%d', time.localtime()),
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
            'processors': ['first', 'taoche.mile'],
        },
        'volume': {
            'xpath': (
                after_has(u'发 动 机'),
            ),
        },
        'control': {
            'xpath': (
                after_has(u'变 速'),
            ),
        },
        'price': {
            'xpath': (
                attr(id_('hidPrice'), 'value'),
            ),
        },
        'price_bn': {
            'xpath': (
                text(cls('jagfcbox', '/p[2]/')),
            ),
            'processors': ['join'],
        },
        'brand_slug': {
            'xpath': (
                after_has(u'车辆品牌'),
            ),
        },
        'model_slug': {
            'xpath': (
                after_has(u'车辆型号'),
            ),
        },
        'model_url': {
            'xpath': (
                href(cls('tc14-tal', '/a[5]')),
            ),
        },
        'city': {
            'xpath': (
                after_has(u'牌照地点'),
            ),
        },
        'phone': {
            'xpath': (
                attr(cls('tc14-cydh'), 'style'),
            ),
            'regex': '(http://cache.taoche.com/buycar/gettel.ashx\?u=\d+&t=\w+)[,&]',
        },
        'contact': {
            'xpath': (
                u'//*[@id="divParaTel"]/p[last()]/text()',
            ),
            'regex': r'([^\(\[\s]{1,4})[\(\[\s]?',
            'processors': ['join'],
        },
        'region': {
            'xpath': (
                u'//*[contains(@class,"cycsrzbox")]//*[contains(text(), "地址")]/following-sibling::text()',
            ),
            'before': '[',
        },
        'company_name': {
            'xpath': (
                '//*[contains(@class,"cycsrzbox")]//h3/a/text()',
            ),
            'processors': ['last'],
        },
        'company_url': {
            'xpath': (
                href(cls('cyssbut', '/span/a')),
            ),
        },
        'quality_service': {
            'xpath': (
                u'//*[@id="divFuwuContainer"]//*[contains(text(), "质保") or contains(text(), "延保")]/text()',
            ),
            'processors': ['join'],
        },
        'description': {
            'xpath': (
                text(cls('chyxx_text')),
            ),
            'processors': ['first', 'taoche.description'],
        },
        'imgurls': {
            'xpath': (
                '//div[@class="cyxqpicdown"]//*[@class="carpicbox"]/img/@data-src',
                '//div[@class="cyxqpicdown"]//*[@class="carpicbox"]/img/@src',
            ),
            'processors': ['join'],
        },
        'mandatory_insurance': {
            'xpath': (
                u'//*[contains(text(), "保险到期") or contains(text(), "交强险到期")]/text()',
            ),
        },
        'examine_insurance': {
            'xpath': (
                has(u'年检到期', '/..'),
            ),
        },
        'transfer_owner': {
            'xpath': (
                u'//*[contains(text(), "过户次数")]/span/text()',
            ),
            'regex': ur'(\d+)次',
        },
        'car_application': {
            'xpath': (
                has(u'车辆类型', '/..'),
            ),
        },
        'source_type': {
            'xpath': [
                attr(cls('cycs-logo', '/a/img'), 'src'),  # 3、品牌认证车商
                href(cls('cyssbut', '/span/a')),         # 5、普通车商
            ],
            'processors': ['taoche.source_type'],
            'default': SOURCE_TYPE_GONGPINGJIA,
        },
        'is_certifield_car': {
            'default': '%(quality_service)s',
        },
    },
}

parse_rule = {
    'url': {
        # 'xpath': (
        #     url(has_cls('cary-infor', '/h3')),
        #     '//*[@id="logwtCarList"]//div[@class="cary-infor"]/h3/a[@href]/@href',
        # ),
        're': (
            r'http://www.taoche.com/buycar/\w-[\d\w]+\.html',
        ),
        'step': 'parse_detail',
        # 'format': '{0}?page=72',
    },
    'list_url': {
        're': (
            r'http://www.taoche.com/v\d+/',
        ),
        'format': '{0}car/?ob=createtime-',
        'step': 'parse_list',
        'dont_filter': False,
    },
    'next_page_url': {
        'xpath': (
            '//a[@class="next_on"]/@href',
            url(after('*[@id="logwtdealer"]//li[@class="current"]', '*')),
        ),
        'step': 'parse',
        'format': True,
        # 'max_pagenum': 25,
        # 'incr_pageno': 5,
    },
}

parse_list = {
    'url': {
        're': (
            r'http://www.taoche.com/buycar/\w-[\d\w]+\.html',
        ),
        'step': 'parse_detail',
    },
    'next_page_url': {
        'xpath': (
            next_page(),
        ),
        'excluded': ['javascript'],
        'format': True,
        'step': 'parse_list',
        'dont_filter': False,
    },
}

rule = {
    'name': u'二手车之家',
    'domain': 'taoche.com',
    'base_url': 'http://www.taoche.com',
    'per_page': 50,
    'pages': 2000,
    'pages': 9000,
    'dealer': {
        'url': '%scar/?ob=createtime-',
    },
    'start_urls': [
        # 'http://www.taoche.com/all/?orderid=5&direction=2&onsale=1',
        'http://www.taoche.com/all/?orderid=5&direction=2',
        # 'http://www.taoche.com/all/?page=36',
        # 'http://www.taoche.com/all/?page=216',
        # 'http://www.taoche.com/buycar/pges5bxcdza/?page=216',
        # 'http://www.taoche.com/buycar/pges3bxcdza/?page=216',
        # 'http://www.taoche.com/buycar/pges2bxcdza/?page=216',
        # 'http://www.taoche.com/buycar/pges1bxcdza/?page=216',
        # Debug details
        # 'http://www.taoche.com/buycar/b-DealerYQDZ1166107S.html',
        # 'http://www.taoche.com/buycar/b-Dealer15060815359.html',
        # 'http://www.taoche.com/buycar/p-5860783.html',
        # 'http://www.taoche.com/buycar/b-DealerAUDI1080088S.html',
        # 'http://www.taoche.com/buycar/b-Dealer15032612396.html',
        # 'http://www.taoche.com/buycar/b-Dealer15040911803.html',
        # 'http://www.taoche.com/buycar/b-Dealer15041113418.html',
        # 'http://www.taoche.com/buycar/b-Dealer15041214906.html',
        # 'http://www.taoche.com/buycar/p-6373146.html', # 个人
        # 'http://www.taoche.com/buycar/b-DealerJZG1208505T.html', # 商家
        # 'http://www.taoche.com/buycar/b-Dealer15050414791.html', # 商家保障
        # 'http://www.taoche.com/buycar/b-Dealer15051214896.html', # 品牌认证
        # 'http://www.taoche.com/buycar/b-Dealer15070314453.html', # 里程为 百公里内
        # 'http://www.taoche.com/buycar/p-6872642.html',  # phone is null
        # 'http://www.taoche.com/buycar/b-Dealer15090115833.html',  # car_application is null
    ],

    'parse': parse_rule,
    'parse_list': parse_list,
    'parse_detail': {
        'item': item_rule,
    }
}

fmt_rule_urls(rule)
# rule['parse'] = rule['parse_detail']
