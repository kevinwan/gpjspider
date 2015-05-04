# -*- coding: utf-8 -*-
from .utils import *
from gpjspider.utils.constants import SOURCE_TYPE_GONGPINGJIA


def parse_meta(key, with_key=False):
    return with_key and u'(%s[^：]{,4}：[^;\s]+)' % key or u'%s[^：]{,4}：([^;\s]+)' % key


item_rule = {
    'class': 'UsedCarItem',
    'keys': [
        'meta', 'title', 'dmodel', 'city', 'brand_slug', 'model_slug',
        'volume', 'year', 'month', 'mile', 'control', 'color', 'price_bn',
        'price', 'transfer_owner', 'car_application', 'mandatory_insurance', 'business_insurance', 'examine_insurance',
        'company_name', 'company_url', 'phone', 'contact', 'region', 'description', 'imgurls',
        'maintenance_record', 'maintenance_desc', 'quality_service', 'driving_license', 'invoice',
        'time', 'is_certifield_car', 'source_type',
    ],
    # 'debug': 'is_certifield_car',
    'fields': {
        'meta': {
            'xpath': (
                '//meta[@name="description" or @name="Description"]/@content',
            ),
            'processors': ['first'],
        },
        'title': {
            'xpath': (
                '//h2[@class="title"]/text()',
                # '//div[@class="car-info"]/h2/@title',
                # '//div[@class="lixdianh_left"]/h2/text()',
                # '/html/head/title/text()',
            ),
            'processors': ['first'],
            'required': True,
        },
        'dmodel': {
            # 'xpath': (
            #     '//div[@class="tc14-cyxq-tit"]/h3/text()',
            #     '/html/head/title/text()',
            # ),
            'default': '%(title)s',
            # 'default': '{title}',
            'after': '-',
            'processors': ['first'],
            # 'processors': ['join'],
        },
        'time': {
            'xpath': (
                has(u'发布时间'),
                u'//*[contains(text(), "发布时间")]/following-sibling::*/text()',
                # '//*[id="ulParaDetails"]/preceding-sibling::*/text()',
                # '//*[@class="time"]/text()',
            ),
            'processors': ['first', 'after_colon', 'gpjtime'],
        },
        'is_certifield_car': {
            'xpath': (
                text(with_cls('renzheng')),
                # '//div[@class="cycsrz" or @class="xbfwicobox"]//text()',
                # '//div[@class="cycsrz" or @class="yichebaoz"]//text()',
                # '//*[@class="cycsrz" or @class="yichebaoz"]//text()',
                # '//div[@class="cycsrz" or @class="yichebaoz"]//text()',
                # 'boolean(//div[@class="cycsrz"]//text() | //div[@class="yichebaoz"]//text())',
                # 'boolean(//div[@class="yichebaoz"]//text())',
                # '//div[@class="part4"]//text()',
                # for autonomous cars
                # '//div[@class="assess-ul"]//text()',
            ),
            'processors': ['concat', 'is_certified'],
            'processors': ['first', 'is_certified'],
            # 'default': False,
        },
        'source_type': {
            'xpath': (
                text(with_cls('renzheng')),
                # '//*[@id="hidUcarSerialNumber"]/@value | //div[@class="cycsrz" or @class="xbfwicobox"]//text()',
                # '//*[@id="hidUcarSerialNumber"]/@value | //div[@class="cycsrz" or @class="yichebaoz"]//text()',
                # '//div[@class="cycsrz"]/text() | //div[@class="yichebaoz"]//text()',
                # '//meta[@http-equiv="mobile-agent"]/@content | //div[@class="part4"]//text()',
            ),
            'processors': ['concat', 'taoche.source_type'],
            'processors': ['first', 'sohu.source_type'],
            # 'default': '%(source_info)s',
            # 'default': SOURCE_TYPE_GONGPINGJIA,
        },
        'city': {
            'xpath': (
                u'//*[@class="your-position"]/following-sibling::*[1]//text()',
                # '//div[@class="breadnav"]/a[2]/text()',
            ),
            # 'default': '%(meta)s',
            # 'regex': parse_meta(u'车源所在地'),
            # 'processors': ['first'],
            'processors': ['concat', 'city'],
        },
        'brand_slug': {
            'xpath': (
                u'//*[@class="your-position"]/following-sibling::*[last()-2]//text()',
                # u'//*[contains(text(), "车辆品牌")]/following-sibling::*/text()',
                # '//div[@class="breadnav"]/a[last()-1]/text()',
            ),
            # 'regex': ur'二手(.*)',
            'after': u'二手',
            'processors': ['join', 'brand_slug'],
        },
        'model_slug': {
            'xpath': (
                u'//*[@class="your-position"]/following-sibling::*[last()-1]//text()',
                # u'//*[contains(text(), "车辆型号")]/following-sibling::*/text()',
                # '//div[@class="breadnav"]/a[last()]/text()',
            ),
            'after': u'二手',
            'processors': ['join', 'model_slug']
        },
        'volume': {
            # 'xpath': (
            #     u'//*[contains(text(), "发 动 机")]/following-sibling::*/text()',
            # u'//*[contains(text(), "发 动 机")]/span/text() | //*[@id="car_carname"]/@value',
            # ),
            # 'processors': ['concat'],
            'default': '%(meta)s',
            'regex': parse_meta(u'排气量'),
        },
        'year': {
            # 'xpath': (
            #     u'//*[@id="hidBuyCarDate"]/@value | //*[contains(text(), "上牌")]/following-sibling::text()',
            # u'//*[contains(text(), "上牌")]/text()',
            # u'//*[@id="car_firstregtime"]/@value',
            # ),
            'default': '%(meta)s',
            'regex': parse_meta(u'上牌'),
        },
        'month': {
            # 'xpath': (
            #     u'//*[@id="hidBuyCarDate"]/@value | //*[contains(text(), "上牌")]/following-sibling::text()',
            # ),
            # 'processors': ['first'],
            'default': '%(meta)s',
            'regex': parse_meta(u'上牌'),
        },
        'mile': {
            # 'xpath': (
            # u'//*[contains(text(), "行驶里程")]/text()',
            #     u'//*[contains(text(), "行驶里程")]/following-sibling::*/text()',
            # ),
            'default': '%(meta)s',
            'regex': parse_meta(u'里程'),
        },
        'price_bn': {
            'xpath': (
                '//*[@id="newCarPriceG"]/@value',
                # '//*[@id="CarNewPrice"]/text()',
                # u'//*[@class="jagfcbox"]/p[2]//text()',
            ),
            'processors': ['first', 'price'],
            # 'default': '%(meta)s',
            # 'regex': parse_meta(u'新车指导价'),
            # 'regex': parse_meta(u'新车', with_key=True),
        },
        'price': {
            'xpath': (
                '//span[@class="price"]/text()',
                # '//*[@id="hidPrice"]/@value',
                # u'//*[contains(text(), "价格")]/following-sibling::p//text()',
            ),
            # 'processors': ['first', 'price'],
        },
        'control': {
            # 'xpath': (
            # u'//*[contains(text(), "变 速 器")]/span/text()',
            #     u'//*[contains(text(), "变 速 ")]/following-sibling::*/text()',
            # u'//*[contains(text(), "变 速 器") | contains(text(), "变 速 箱")]/..//text()',
            # ),
            # 'processors': ['join', 'after_colon', 'strip'],
            'default': '%(meta)s',
            'regex': parse_meta(u'变速箱'),
        },
        'transfer_owner': {
            'xpath': (
                after_has(u'是否一手车'),
                u'//*[contains(text(), "过户次数")]/span/text()',
            ),
            # 'regex': ur'(\d+)次',
            # 'default': '%(meta)s',
            # 'regex': parse_meta(u'是否一手车'),
        },
        'color': {
            # 'xpath': (
            #     u'//*[contains(text(), "颜色")]/text()',
            #     u'/html/body/div[6]/div[3]/div[1]/div[9]/div[2]/ul[1]/li[4]/text()',
            # ),
            # 'processors': ['join', 'after_colon'],
            'default': '%(meta)s',
            'regex': parse_meta(u'颜色'),
        },
        'mandatory_insurance': {
            # 'xpath': (
            # u'//*[match(text(), "(保|交强)险到期")]/text()',
            # u'//*[contains(text(), "(保|交强)险到期")]/text()',
            #     u'//*[contains(text(), "保险到期") or contains(text(), "交强险到期")]/text()',
            # u'//*[contains(text(), "保险")]/text()',
            # ),
            'default': '%(meta)s',
            'regex': parse_meta(u'保险'),
        },
        'business_insurance': {
            'xpath': (
                after_has(u'商业险'),
                # u'//*[contains(text(), "商业险")]/text()',
            ),
            'processors': ['first', 'year_month'],
            # 'default': '%(meta)s',
            # 'regex': parse_meta(u'商业险'),
        },
        'examine_insurance': {
            # 'xpath': (
            #     u'//*[contains(text(), "年检")]/following-sibling::text()',
            # ),
            # 'processors': ['first', 'year_month'],
            'default': '%(meta)s',
            'regex': parse_meta(u'年检'),
        },
        'car_application': {
            # 'xpath': (
            #     u'//*[contains(text(), "车辆类型")]/following-sibling::text()',
            # u'//*[contains(text(), "用途")]/text()',
            # ),
            # 'processors': ['first'],
            'default': '%(meta)s',
            'regex': parse_meta(u'使用性质'),
        },
        # condition_level
        # condition_detail
        # 'maintenance_record': {
        #     'xpath': (
        #         u'boolean(//*[contains(text(), "定期保养") or contains(text(), "定期4S保养")])',
        #         u'boolean(//*[contains(text(), "保养")])',
        #     ),
        #     'processors': ['first', 'has_maintenance_record'],
        # },
        'maintenance_desc': {
            'xpath': (
                after_has(u'保养'),
                u'//*[contains(text(), "保养")]/text()',
            ),
            # 'processors': ['first', 'after_colon'],
        },
        'quality_service': {
            'xpath': (
                u'//*[@id="divFuwuContainer"]//*[contains(text(), "质保") or contains(text(), "延保")]/text()',
                # u'//*[@id="divFuwuContainer"]//div[@class="xbfwicobox"]//text()',
                # u'//*[@class="cyxqpicdown"]//p[contains(text(), "包退") or contains(text(), "质保") or contains(text(), "延保")]/text()',
                # u'//*[contains(text(), "质保") or contains(text(), "延保")]/text()',
            ),
            # 'after': '.',
            # 'processors': ['quality_service'],
            # 'processors': ['last'],
            'processors': ['join'],
        },
        'driving_license': {
            'xpath': (
                after_has(u'行驶证'),
                u'//*/span[contains(text(), "行驶证")]/../text()',
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
                # '//div[@class="cyxqpicdown"]//*[@class="carpicbox"]/img/@src',
                # '//div[@class="explain"]//*[@class="pic-box"]/img/@src',
            ),
            'processors': ['join'],
        },
        'company_name': {
            'xpath': (
                string('dt[@class="title"]/a'),
                # '//*[contains(@class,"cycsrzbox")]//h3/a/text()',
            ),
            # 'processors': ['last'],
        },
        'company_url': {
            'xpath': (
                url('dt[@class="title"]'),
                # '//*[contains(@class,"cycsrzbox")]//h3/a/@href',
                # '//div[@class="cyssbut"]/a/@href',
            ),
            'format': True,
            # 'processors': ['first'],
        },
        'phone': {
            'xpath': (
                '//*[@class="phone"]/text()',
                # u'//*[contains(@class,"cycsrzbox")]//*[contains(text(), "电话")]/following-sibling::text()',
                # '//*[@id="carOwnerInfo"]/div[1]/div[1]//img/@src',
            ),
            # 'regex': '(http://cache.taoche.com/buycar/gettel.ashx\?u=\d+&t=\w+)[,&]',
            # 'format': 'http://www.taoche.com{0}',
            # 'processors': ['first', 'taoche.phone'],
        },
        'contact': {
            'xpath': (
                has(u'联系人'),
                # u'//*[@id="divParaTel"]/p[last()]/text()',
                # u'//*[@id="carOwnerInfo"]/div[1]/div[last()-1]/text()',
            ),
            # 'regex': r'([^\(\[\s]{1,4})[\(\[\s]?',
            'processors': ['join'],
            'processors': ['first', 'after_colon'],
        },
        'region': {
            'xpath': (
                # has(u'地址', prefix='*[@class="address"]//'),
                u'//*[@class="address"]/text()',
                # u'//*[contains(@class,"cycsrzbox")]//*[contains(text(), "地址")]/following-sibling::text()',
                # '//*[@id="carOwnerInfo"]/div[1]/div[last()]/text()',
            ),
            # 'before': '[',
            'processors': ['first', 'after_colon', 'strip'],
            'processors': ['last'],
        },
        'description': {
            # 'xpath': (
            #     after_has(u'车况介绍'),
            #     '//div[@class="cyxqpicdown"]//*[@class="chyxx_text"]/text()',
            #     '//div[@class="explain"]/p[1]/text()',
            # ),
            'default': '%(meta)s',
            'after': u'车况介绍：',
        },

    },
}

parse_rule = {
    'url': {
        'xpath': (
            url('*[@class="item"]//div[@class="pic"]'),
            # url('*[@class="all-source"]//div[@class="pic"]'),
        ),
        # 'match': '/buycar/carinfo',
        'contains': ['/buycar/carinfo'],
        # 'excluded': ['/autonomous/'],
        'format': True,
        'processors': ['clean_anchor'],
        'step': 'parse_detail',
        # 'update': True,
        # 'category': 'usedcar',
    },
    'next_page_url': {
        'xpath': (
            # url('div[@class="pager"]'),
            url('*[@class="no"][last()]'),
            # '//div[@class="page"]/@href',
            # '//a[@class="page-item-next"]/@href',
            # '//a[@class="next_on"]/@href',
        ),
        'format': True,
        # 'max_pagenum': 50000,
        # 'match': '/pg\d+.shtml',
        'step': 'parse',
    },
}

rule = {
    'name': u'搜狐二手车',
    'domain': '2sc.sohu.com',
    'base_url': 'http://2sc.sohu.com',

    'start_urls': [
        'http://2sc.sohu.com/buycar/a0b0c0d0e0f0g0h3j0k0m0n0/',
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
    ],

    'parse': parse_rule,
    # 'parse_list': parse_rule,
    'parse_detail': {
        'item': item_rule,
    },
}


def fmt_urls(rule, base_url=rule['base_url']):
    for k, v in rule.items():
        if 'url' in k and v.get('format'):
            v['format'] = to_url(base_url)

fmt_urls(rule['parse'])
fmt_urls(item_rule['fields'])
