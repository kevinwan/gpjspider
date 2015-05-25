# -*- coding: utf-8 -*-
from .utils import *


item_rule = {
    'class': 'UsedCarItem',
    'fields': {
        'title': {
            'xpath': (
                '//div[@class="car-info"]/h2/@title',
            ),
            'required': True,
        },
        'meta': {
            'xpath': (
                '//meta[@name="description" or @name="Description"]/@content',
            ),
        },
        'time': {
            'xpath': (
                '//div[@class="time"]/text()',
            ),
            'processors': ['first', 'gpjtime'],
        },
        'year': {
            'xpath': (
                # u'//*[contains(text(), "上牌")]/text()',
                u'//*[@id="car_firstregtime"]/@value',
            ),
        },
        'month': {
            'xpath': (
                u'//*[@id="car_firstregtime"]/@value',
            ),
        },
        'mile': {
            'xpath': (
                u'//*[contains(text(), "行驶里程")]/text()',
            ),
            'processors': ['first', 'after_colon', 'mile'],
        },
        'volume': {
            'xpath': (
                u'//*[contains(text(), "发 动 机")]/span/text() | //*[@id="car_carname"]/@value',
                # u'//*[@id="car_carname"]/@value',
            ),
        },
        'color': {
            'xpath': (
                # u'//*[contains(text(), "颜色")]/text()',
                u'/html/body/div[6]/div[3]/div[1]/div[9]/div[2]/ul[1]/li[4]/text()',
            ),
            'processors': ['first', 'after_colon'],
        },
        'control': {
            'xpath': (
                u'//*[contains(text(), "变 速 器")]/span/text()',
                # u'/html/body/div[6]/div[3]/div[1]/div[9]/div[2]/ul[1]/li[2]/text()',
            ),
            'processors': ['first', 'after_colon'],
        },
        'price': {
            'xpath': (
                '//span[@class="font30"]/text()',
            ),
        },
        'price_bn': {
            'xpath': (
                '//*[@id="CarNewPrice"]/text()',
            ),
        },
        'brand_slug': {
            'xpath': (
                '//div[@class="breadnav"]/a[last()-1]/text()',
            ),
        },
        'model_slug': {
            'xpath': (
                '//div[@class="breadnav"]/a[last()]/text()',
            ),
        },
        'city': {
            'xpath': (
                '//div[@class="breadnav"]/a[2]/text()',
            ),
        },
        'phone': {
            'xpath': (
                '//*[@id="carOwnerInfo"]/div[1]/div[1]//img/@src',
            ),
            'format': True,
        },
        'contact': {
            'xpath': (
                u'//*[@id="carOwnerInfo"]/div[1]/div[last()-1]/text()',
            ),
            'regex': r'([^\(\[]{1,4})[\(\[]?',
        },
        'region': {
            'xpath': (
                '//*[@id="carOwnerInfo"]/div[1]/div[last()]/text()',
            ),
        },
        'company_name': {
            'xpath': (
                '//div[@class="merchant-name"]/a/text()',
            ),
        },
        'company_url': {
            'xpath': (
                '//div[@class="merchant-name"]/a/@href',
            ),
            'format': True,
            'processors': ['first', 'clean_anchor'],
        },
        # 'driving_license': {
        #     'xpath': (
        #         u'//li/span[contains(text(), "行驶证")]/../text()',
        #     ),
        # },
        # 'invoice': {
        #     'xpath': (
        #         u'//li/span[contains(text(), "购车发票")]/../text()',
        #     ),
        # },
        # 'maintenance_record': {
        #     'xpath': (
        #         u'//li[contains(text(), "保养")]/text()',
        #     ),
        #     'processors': ['first', 'after_colon'],
        # },
        'maintenance_desc': {
            'xpath': (
                u'//li[contains(text(), "保养")]/text()',
            ),
            'processors': ['first', 'after_colon'],
        },
        'quality_service': {
            'xpath': (
                u'//li[contains(text(), "质保") or contains(text(), "延保")]//text()',
            ),
            'processors': ['quality_service'],
        },
        'description': {
            'xpath': (
                '//div[@class="explain"]/p[1]/text()',
            ),
            'processors': ['join'],
        },
        'imgurls': {
            'xpath': ('//div[@class="explain"]/div[@class="pic-box"]/img/@src',),
            'processors': ['join'],
        },
        'mandatory_insurance': {
            'xpath': (
                u'//li[contains(text(), "保险")]/text()',
            ),
        },
        # 'business_insurance': {
        #     'xpath': (
        #         u'//li[contains(text(), "商业险")]/text()',
        #     ),
        # },
        'examine_insurance': {
            'xpath': (
                u'//li[contains(text(), "年检")]/text()',
            ),
        },
        'transfer_owner': {
            'xpath': (
                u'//li[contains(text(), "过户次数")]/span/text()',
            ),
            'regex': ur'(\d+)次',
        },
        'car_application': {
            'xpath': (
                # u'//li[contains(text(), "用途")]/text()',
                u'//*[@id="divHistory"]/div[2]/ul/li[6]/text()',
            ),
            'processors': ['first', 'after_colon'],
        },
        'source_type': {
            'xpath': (
                '//meta[@http-equiv="mobile-agent"]/@content | //div[@class="part4"]//text()',
            ),
            'processors': ['concat', 'che168.source_type'],
            'default': SOURCE_TYPE_GONGPINGJIA,
        },
        'is_certifield_car': {
            'xpath': (
                '//div[@class="part4"]//text()',
                # for autonomous cars
                # '//div[@class="assess-ul"]//text()',
            ),
            'processors': ['concat'],
            'default': False,
        },
    },
}

rule = {
    # ==========================================================================
    #  基本配置
    # ==========================================================================
    'name': u'二手车之家',
    'domain': 'che168.com',
    'base_url': 'http://www.che168.com',
    'start_urls': [
        'http://www.che168.com/china/list/',
        # 'http://www.che168.com/china/a0_0ms3dgscncgpiltocspex/',
        # 'http://www.che168.com/china/a0_0ms4dgscncgpiltocspex/',
        # 'http://www.che168.com/china/a0_0ms2dgscncgpiltocspex/',
        # 'http://www.che168.com/china/a0_0ms1dgscncgpiltocspex/',
        # For Debug details
        # 'http://www.che168.com/dealer/100582/4821401.html',
        # 'http://www.che168.com/dealer/134677/4756499.html',
        # 'http://www.che168.com/dealer/69682/4141834.html',
        # 'http://www.che168.com/dealer/85459/4807434.html',
        # 'http://www.che168.com/personal/4323708.html',
        # 'http://www.che168.com/personal/4799037.html',
        # 'http://www.che168.com/dealer/162138/4821871.html',
        # 'http://www.che168.com/dealer/128393/4786037.html',
        # 'http://www.che168.com/autonomous/4743579.html',
    ],

    # ==========================================================================
    #  默认步骤  parse
    # ==========================================================================
    'parse': {
        'url': {
            'xpath': (
                '//*[@class="all-source"]//div[@class="pic"]/a[@href]/@href',
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
    },
    # ==========================================================================
    #  详情页步骤  parse_list
    # ==========================================================================
    # 'parse_list': {
    #     'url': {
    #         're': (r'http.*58.com/ershouche/.*\.shtml',),
    # 新 url 对应的解析函数
    #         'step': 'parse_detail',
    #         'update': True,
    #         'category': 'usedcar'
    #     },
    #     'next_page_url': {
    #         'xpath': ('//a[@class="next"]/@href', ),
    #         'format': 'http://quanguo.58.com{0}',
    #         'step': 'parse_list',
    #     },
    # },

    # ==========================================================================
    #  详情页步骤  parse_detail
    # ==========================================================================
    'parse_detail': {
        'item': item_rule,
    }
}

fmt_rule_urls(rule)
