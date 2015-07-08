# -*- coding: utf-8 -*-
from .utils import *
import time

item_rule = {
    'class': 'UsedCarItem',
    'fields': {
        'title': {
            'xpath': (
                text(cls('tc14-cyxq-tit', '/h3')),
                #'//div[@class="tc14-cyxq-tit"]/h3//text()',
            ),
            'processors': ['join'],
            'after': ' - ',
            'required': True,
        },
        'dmodel': {
            #'xpath': (
                #'//div[@class="tc14-cyxq-tit"]/h3/text()',
                #'/html/head/title/text()',
            #),
            'default': '%(title)s',
            #'processors': ['join'],
        },
        'meta': {
            'xpath': (
                '//meta[@name="description" or @name="Description"]/@content',
            ),
        },
        'time': {
            'xpath': (
                text(cls('tc14-tabtitbox tc14-tab-h53  tc14-cytab clearfix', '/span')),
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
                #u'//*[contains(text(), "发 动 机")]/following-sibling::*/text()',
            ),
        },
        'control': {
            'xpath': (
                after_has(u'变 速'),
                #u'//*[contains(text(), "变 速 ")]/following-sibling::*/text()',
            ),
        },
        'price': {
            'xpath': (
                attr(id_('hidPrice'), 'value'),
                #'//*[@id="hidPrice"]/@value',
            ),
        },
        'price_bn': {
            'xpath': (
                #u'//*[@class="jagfcbox"]/p[2]//text()',
                text(cls('jagfcbox', '/p[2]/')),
            ),
            'processors': ['join'],
        },
        'brand_slug': {
            'xpath': (
                #u'//*[contains(text(), "车辆品牌")]/following-sibling::*/text()',
                #'//div[@class="breadnav"]/a[last()-1]/text()',
                after_has(u'车辆品牌'),
            ),
        },
        'model_slug': {
            'xpath': (
                #u'//*[contains(text(), "车辆型号")]/following-sibling::*/text()',
                #'//div[@class="breadnav"]/a[last()]/text()',
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
                #u'//*[contains(text(), "牌照地点")]/following-sibling::*/text()',
                #'//div[@class="breadnav"]/a[2]/text()',
                after_has(u'牌照地点'),
            ),
        },
        'phone': {
            'xpath': (
                #'//*[@class="tc14-cydh"]/@style',
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
                #'//*[contains(@class,"cycsrzbox")]//h3/a/@href',
                #'//div[@class="cyssbut"]/a/@href',
            ),
        },
        #'maintenance_record': {
            #'xpath': (
                #u'boolean(//*[contains(text(), "定期保养") or contains(text(), "定期4S保养")])',
            #),
            #'processors': ['first', 'has_maintenance_record'],
        #},
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
                #u'//*[contains(text(), "年检")]/following-sibling::text()',
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
                #u'//*[contains(text(), "车辆类型")]/following-sibling::text()',
                after_has(u'车辆类型'),
            ),
            #'processors': ['first', 'after_colon'],
        },
        'source_type': {
            'xpath': [
                attr(cls('cycs-logo', '/a/img'), 'src'), # 3、品牌认证车商
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

rule = {
    # ==========================================================================
    #  基本配置
    # ==========================================================================
    'name': u'二手车之家',
    'domain': 'taoche.com',
    'base_url': 'http://www.taoche.com',
    'start_urls': [
        'http://www.taoche.com/all/?orderid=5&direction=2&onsale=1',
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
        #'http://www.taoche.com/buycar/p-6373146.html', # 个人
        #'http://www.taoche.com/buycar/b-DealerJZG1208505T.html', # 商家
        #'http://www.taoche.com/buycar/b-Dealer15050414791.html', # 商家保障
        #'http://www.taoche.com/buycar/b-Dealer15051214896.html', # 品牌认证
        #'http://www.taoche.com/buycar/b-Dealer15070314453.html', # 里程为 百公里内
    ],
    'per_page': 50,
    'pages': 2000,
    'pages': 9000,

    # ==========================================================================
    #  默认步骤  parse
    # ==========================================================================
    'parse': {
        'url': {
            'xpath': (
                url(has_cls('cary-infor', '/h3')),
                '//*[@id="logwtCarList"]//div[@class="cary-infor"]/h3/a[@href]/@href',
            ),
            'step': 'parse_detail',
            # 'format': '{0}?page=72',
            # 'update': True,
            # 'category': 'usedcar',
        },
        'next_page_url': {
            'xpath': (
                '//a[@class="next_on"]/@href',
                url(after('*[@id="logwtdealer"]//li[@class="current"]', '*')),
            ),
            'step': 'parse',
            # 'processors': ['clean_param'],
            'format': True,
            # 'max_pagenum': 25,
            # 'incr_pageno': 5,
        },
    },

    # ==========================================================================
    #  详情页步骤  parse_detail
    # ==========================================================================
    'parse_detail': {
        'item': item_rule,
    }
}

fmt_rule_urls(rule)
# rule['parse'] = rule['parse_detail']
