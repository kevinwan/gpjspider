# -*- coding: utf-8 -*-
from .utils import *

tag = lambda i: text('*[@id="sift"]/div[3]/div[2]/p[3]/span[2]/i[%s]' % i)

item_rule = {
    'class': 'UsedCarItem',
    'fields': {
        'title': {
            'xpath': (
                '//div[@class="car-info"]/h2/@title',
                text(with_cls('info', '/h3/a')),
            ),
            'required': True,
        },
        'meta': {
            'xpath': (
                '//meta[@name="description" or @name="Description"]/@content',
                text(with_cls('text')),
            ),
        },
        'time': {
            'xpath': (
                # '//div[@class="time"]/text()',
                has(u'发布日期'),
                text(with_cls('time')),
            ),
            # 'processors': ['first', 'gpjtime'],
        },
        'year': {
            'xpath': (
                # u'//*[contains(text(), "上牌")]/text()',
                tag(5),
                u'//*[@id="car_firstregtime"]/@value',
            ),
        },
        'month': {
            'xpath': (
                tag(5),
                u'//*[@id="car_firstregtime"]/@value',
            ),
        },
        'mile': {
            'xpath': (
                # after_has(u'车型概括'),
                tag(4),
                u'//*[contains(text(), "行驶里程")]/text()',
            ),
            # 'processors': ['first', 'after_colon', 'mile'],
        },
        'volume': {
            'xpath': (
                hidden('pailiang'),
                tag(3),
                u'//*[contains(text(), "发 动 机")]/span/text() | //*[@id="car_carname"]/@value',
                # u'//*[@id="car_carname"]/@value',
            ),
        },
        'color': {
            'xpath': (
                # u'//*[contains(text(), "颜色")]/text()',
                tag(1),
                u'/html/body/div[6]/div[3]/div[1]/div[9]/div[2]/ul[1]/li[4]/text()',
            ),
            'processors': ['first', 'after_colon'],
        },
        'control': {
            'xpath': (
                tag(2),
                u'//*[contains(text(), "变 速 器")]/span/text()',
                # u'/html/body/div[6]/div[3]/div[1]/div[9]/div[2]/ul[1]/li[2]/text()',
            ),
            'processors': ['first', 'after_colon'],
        },
        'price': {
            'xpath': (
                text(with_cls('price')),
                '//span[@class="font30"]/text()',
            ),
        },
        'price_bn': {
            'xpath': (
                text(id_('CarNewPrice')),
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
                text(with_cls('nav-bread', '/a[2]')),
                '//div[@class="breadnav"]/a[last()]/text()',
            ),
        },
        'city': {
            'xpath': (
                has(u'车辆所在地'),
                '//div[@class="breadnav"]/a[2]/text()',
            ),
        },
        'phone': {
            'xpath': (
                attr(id_('callPhone'), 'data-telno'),
                '//*[@id="carOwnerInfo"]/div[1]/div[1]//img/@src',
            ),
            'format': True,
            'default': '%(meta)s',
            'regex': u'致电(\d+)',
        },
        'contact': {
            'xpath': (
                text(with_cls('info')),
                u'//*[@id="carOwnerInfo"]/div[1]/div[last()-1]/text()',
            ),
            'processors': ['last'],
            'regex': r'([^\(\[]{1,4})[\(\[]?',
        },
        'region': {
            'xpath': (
                '//*[@id="carOwnerInfo"]/div[1]/div[last()]/text()',
            ),
            'default': '%(meta)s',
            'regex': u'地址：(.+)。',
            'regex_fail': '',
        },
        'company_name': {
            'xpath': (
                has(u'商家名称'),
                '//div[@class="merchant-name"]/a/text()',
            ),
            'after': u'：',
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
                # text('*[@id="sift"]/div[3]/div[7]/div[1]'),
                # text(with_cls('text')),
                '//div[@class="explain"]/p[1]/text()',
            ),
            # 'processors': ['join'],
            'default': '%(meta)s',
        },
        'imgurls': {
            'xp'
            'xpath': (
                attr(with_cls('img', '/a/img'), 'src'),
                '//div[@class="explain"]/div[@class="pic-box"]/img/@src',
            ),
            'processors': ['join'],
        },
        'mandatory_insurance': {
            'xpath': (
                # u'//li[contains(text(), "保险")]/text()',
                has(u'交强险'),
                has(u'保险'),
            ),
        },
        # 'business_insurance': {
        #     'xpath': (
        #         u'//li[contains(text(), "商业险")]/text()',
        #     ),
        # },
        'examine_insurance': {
            'xpath': (
                # u'//li[contains(text(), "年检")]/text()',
                has(u'下次验车'),
                has(u'年检'),
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
        # 'http://m.che168.com/china/0-0-0-6-0-0-00/',
        # 'http://www.che168.com/china/list/',
        # 'http://www.che168.com/china/a0_0ms3dgscncgpiltocspex/',
        # 'http://www.che168.com/china/a0_0ms4dgscncgpiltocspex/',
        # 'http://www.che168.com/china/a0_0ms2dgscncgpiltocspex/',
        # 'http://www.che168.com/china/a0_0ms1dgscncgpiltocspex/',
        # For Debug details
        # 'http://m.che168.com/dealer/201923/5000779.html',
        'http://m.che168.com/dealer/77710/5032736.html',
        # 'http://m.che168.com/dealer/130861/5008532.html',
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
start_url = rule['start_urls'][0]
if ('html' in start_url and len(start_url) > 40) \
        or rule['parse']['url']['contains'][0] in start_url:
    rule['parse'] = rule['parse_detail']
