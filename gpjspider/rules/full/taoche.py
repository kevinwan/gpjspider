# -*- coding: utf-8 -*-
from gpjspider.utils.constants import SOURCE_TYPE_GONGPINGJIA


item_rule = {
    'class': 'UsedCarItem',
    'fields': {
        'title': {
            'xpath': (
                '//div[@class="tc14-cyxq-tit"]/h3//text()',
                '/html/head/title/text()',
            ),
            'processors': ['join', 'strip'],
            'required': True,
        },
        'dmodel': {
            'xpath': (
                '//div[@class="tc14-cyxq-tit"]/h3/text()',
                '/html/head/title/text()',
            ),
            'after': ' - ',
            'processors': ['join', 'strip'],
        },
        'meta': {
            'xpath': (
                '//meta[@name="description" or @name="Description"]/@content',
            ),
            'processors': ['first'],
        },
        'year': {
            'xpath': (
                u'//*[@id="hidBuyCarDate"]/@value | //*[contains(text(), "上牌")]/following-sibling::text()',
            ),
            'processors': ['first', 'year'],
        },
        'month': {
            'xpath': (
                u'//*[@id="hidBuyCarDate"]/@value | //*[contains(text(), "上牌")]/following-sibling::text()',
            ),
            'processors': ['first', 'month'],
        },
        'mile': {
            'xpath': (
                u'//*[contains(text(), "行驶里程")]/following-sibling::*/text()',
            ),
            'processors': ['first', 'mile'],
        },
        'volume': {
            'xpath': (
                u'//*[contains(text(), "发 动 机")]/following-sibling::*/text()',
            ),
            'processors': ['first', 'volume'],
        },
        'control': {
            'xpath': (
                u'//*[contains(text(), "变 速 ")]/following-sibling::*/text()',
            ),
            'processors': ['first'],
        },
        'price': {
            'xpath': (
                '//*[@id="hidPrice"]/@value',
            ),
            'processors': ['first', 'price'],
        },
        'price_bn': {
            'xpath': (
                u'//*[@class="jagfcbox"]/p[2]//text()',
            ),
            'processors': ['join', 'price_bn'],
        },
        'brand_slug': {
            'xpath': (
                u'//*[contains(text(), "车辆品牌")]/following-sibling::*/text()',
                '//div[@class="breadnav"]/a[last()-1]/text()',
            ),
            'processors': ['first', 'brand_slug'],
        },
        'model_slug': {
            'xpath': (
                u'//*[contains(text(), "车辆型号")]/following-sibling::*/text()',
                '//div[@class="breadnav"]/a[last()]/text()',
            ),
            'processors': ['first', 'model_slug']
        },
        'city': {
            'xpath': (
                u'//*[contains(text(), "牌照地点")]/following-sibling::*/text()',
                '//div[@class="breadnav"]/a[2]/text()',
            ),
            'processors': ['first', 'city'],
        },
        'phone': {
            'xpath': (
                '//*[@class="tc14-cydh"]/@style',
            ),
            'regex': '(http://cache.taoche.com/buycar/gettel.ashx\?u=\d+&t=\w+)[,&]',
            'processors': ['first'],
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
            'processors': ['first'],
        },
        'company_name': {
            'xpath': (
                '//*[contains(@class,"cycsrzbox")]//h3/a/text()',
            ),
            'processors': ['last'],
        },
        'company_url': {
            'xpath': (
                '//*[contains(@class,"cycsrzbox")]//h3/a/@href',
                '//div[@class="cyssbut"]/a/@href',
            ),
            'processors': ['first'],
        },
        'maintenance_record': {
            'xpath': (
                u'boolean(//*[contains(text(), "定期保养") or contains(text(), "定期4S保养")])',
            ),
            'processors': ['first', 'has_maintenance_record'],
        },
        'quality_service': {
            'xpath': (
                u'//*[@id="divFuwuContainer"]//*[contains(text(), "质保") or contains(text(), "延保")]/text()',
            ),
            'processors': ['join'],
        },
        'description': {
            'xpath': (
                '//div[@class="cyxqpicdown"]//*[@class="chyxx_text"]/text()',
            ),
            'processors': ['join'],
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
            'processors': ['first', 'year_month'],
        },
        'examine_insurance': {
            'xpath': (
                u'//*[contains(text(), "年检")]/following-sibling::text()',
            ),
            'processors': ['first', 'year_month'],
        },
        'transfer_owner': {
            'xpath': (
                u'//*[contains(text(), "过户次数")]/span/text()',
            ),
            'regex': ur'(\d+)次',
            'processors': ['first', 'gpjint'],
        },
        'car_application': {
            'xpath': (
                u'//*[contains(text(), "车辆类型")]/following-sibling::text()',
            ),
            'processors': ['first', 'after_colon'],
        },
        'source_type': {
            'xpath': (
                '//*[@id="hidUcarSerialNumber"]/@value | //div[@class="cycsrz" or @class="xbfwicobox"]//text()',
            ),
            'processors': ['concat', 'taoche.source_type'],
            'default': SOURCE_TYPE_GONGPINGJIA,
        },
        'is_certifield_car': {
            'xpath': (
                '//div[@class="cycsrz" or @class="xbfwicobox"]//text()',
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
    'domain': 'taoche.com',
    'base_url': 'http://www.taoche.com',
    'start_urls': [
        'http://www.taoche.com/all/',
        # Debug details
        # 'http://www.taoche.com/buycar/p-5860783.html',
        # 'http://www.taoche.com/buycar/b-DealerAUDI1080088S.html',
        # 'http://www.taoche.com/buycar/b-Dealer15032612396.html',
        # 'http://www.taoche.com/buycar/b-Dealer15040911803.html',
        # 'http://www.taoche.com/buycar/b-Dealer15041113418.html',
        # 'http://www.taoche.com/buycar/b-Dealer15041214906.html',
    ],

    # ==========================================================================
    #  默认步骤  parse
    # ==========================================================================
    'parse': {
        'url': {
            'xpath': (
                '//*[@id="logwtCarList"]//div[contains(@class,"cary-infor")]/h3/a[@href]/@href',
            ),
            'step': 'parse_detail',
            'update': True,
            'category': 'usedcar',
        },
        'next_page_url': {
            'xpath': (
                '//a[@class="next_on"]/@href',
            ),
            'step': 'parse',
        },
    },

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
