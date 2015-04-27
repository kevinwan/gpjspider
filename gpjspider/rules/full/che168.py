# -*- coding: utf-8 -*-
from gpjspider.utils.constants import SOURCE_TYPE_GONGPINGJIA


item_rule = {
    'class': 'UsedCarItem',
    'fields': {
        'title': {
            'xpath': (
                '//div[@class="car-info"]/h2/@title',
            ),
            'processors': ['first'],
            'required': True,
        },
        'meta': {
            'xpath': (
                '//meta[@name="description" or @name="Description"]/@content',
            ),
            'processors': ['first'],
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
            'processors': ['first', 'year'],
        },
        'month': {
            'xpath': (
                u'//*[@id="car_firstregtime"]/@value',
            ),
            'processors': ['first', 'month'],
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
            # 'processors': ['first', 'after_colon', 'volume'],
            'processors': ['concat', 'volume'],
            # 'processors': ['first', 'volume'],
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
            'processors': ['first', 'price'],
        },
        'price_bn': {
            'xpath': (
                '//*[@id="CarNewPrice"]/text()',
            ),
            'processors': ['first', 'price_bn'],
        },
        'brand_slug': {
            'xpath': (
                '//div[@class="breadnav"]/a[last()-1]/text()',
            ),
            # 'regex': ur'二手(.*)',
            'processors': ['first', 'brand_slug'],
        },
        'model_slug': {
            'xpath': (
                '//div[@class="breadnav"]/a[last()]/text()',
            ),
            'processors': ['first', 'model_slug']
        },
        'city': {
            'xpath': (
                '//div[@class="breadnav"]/a[2]/text()',
            ),
            'processors': ['first'],
        },
        'phone': {
            'xpath': (
                '//*[@id="carOwnerInfo"]/div[1]/div[1]//img/@src',
            ),
            'format': 'http://www.che168.com{0}',
            'processors': ['first'],
        },
        'contact': {
            'xpath': (
                u'//*[@id="carOwnerInfo"]/div[1]/div[last()-1]/text()',
            ),
            'regex': r'([^\(\[]{1,4})[\(\[]?',
            'processors': ['first'],
        },
        'region': {
            'xpath': (
                '//*[@id="carOwnerInfo"]/div[1]/div[last()]/text()',
            ),
            'processors': ['first'],
        },
        'company_name': {
            'xpath': (
                '//div[@class="merchant-name"]/a/text()',
            ),
            'processors': ['first'],
        },
        'company_url': {
            'xpath': (
                '//div[@class="merchant-name"]/a/@href',
            ),
            'format': 'http://www.che168.com{0}',
            'processors': ['first', 'clean_anchor'],
        },
        # 'driving_license': {
        #     'xpath': (
        #         u'//li/span[contains(text(), "行驶证")]/../text()',
        #     ),
        #     'processors': ['first'],
        # },
        # 'invoice': {
        #     'xpath': (
        #         u'//li/span[contains(text(), "购车发票")]/../text()',
        #     ),
        #     'processors': ['first'],
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
            'processors': ['first', 'year_month'],
        },
        # 'business_insurance': {
        #     'xpath': (
        #         u'//li[contains(text(), "商业险")]/text()',
        #     ),
        #     'processors': ['first', 'year_month'],
        # },
        'examine_insurance': {
            'xpath': (
                u'//li[contains(text(), "年检")]/text()',
            ),
            'processors': ['first', 'year_month'],
        },
        'transfer_owner': {
            'xpath': (
                u'//li[contains(text(), "过户次数")]/span/text()',
            ),
            'regex': ur'(\d+)次',
            'processors': ['first', 'gpjint'],
        },
        'car_application': {
            'xpath': (
                # u'//li[contains(text(), "用途")]/text()',
                u'//*[@id="divHistory"]/div[2]/ul/li[6]/text()',
            ),
            'processors': ['first', 'after_colon'],
        },
        # condition_level
        # condition_detail
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
            'processors': ['concat', 'is_certified'],
            'default': False,
        },
    },
}

rule = {
    # ==========================================================================
    #  基本配置
    # ==========================================================================
    'name': '二手车之家',
    'domain': 'che168.com',
    'base_url': 'http://www.che168.com',
    'start_urls': [
        'http://www.che168.com/china/list/',
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
            'format': 'http://www.che168.com{0}',
            'processors': ['clean_anchor'],
            'step': 'parse_detail',
            'update': True,
            'category': 'usedcar'
        },
        'next_page_url': {
            # 'xpath': ('//div[@class="page"]/@href', ),
            'xpath': (
                '//a[@class="page-item-next"]/@href',
            ),
            'format': 'http://www.che168.com{0}',
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


if rule['start_urls'][0].endswith('.html'):
    p = rule['parse']
    p['item'] = item_rule
    p.pop('next_page_url')
