# -*- coding: utf-8 -*-
from .utils import *
from gpjspider.utils.constants import *

item_rule = {
    "class": "UsedCarItem",
    "fields": {
        'title': {
            'xpath': (
                text(cls('h1')),
                text(id_('cardes')),
            ),
            'required': True,
        },
        'meta': {
            'xpath': (
                '//meta[@name="description" or @name="Description"]/@content',
            ),
        },
        'year': {
            'xpath': (
                has(u'上牌时间', '/span'),
                # has(u'首次上牌'),
                after_has(u'上牌时间'),
            ),
        },
        'month': {
            'xpath': (
                has(u'上牌时间', '/span'),
                # has(u'首次上牌'),
                after_has(u'上牌时间'),
            ),
        },
        'mile': {
            'xpath': (
                # after_has(u'行驶里程'),
                has(u'行驶里程', u'/following-sibling::*[contains(text(), "公里")]'),
                has(u'行驶里程'),
            ),
            'after': u'：',
        },
        'volume': {
            'xpath': (
                after_has(u'排量'),
            ),
            'default': '%(title)s',
        },
        'color': {
            'xpath': (
                has(u'颜色', '/span'),
                after_has(u'颜色'),
            ),
        },
        'control': {
            'xpath': (
                after_has(u'变速箱', 'span'),
            ),
            'default': '%(description)s %(dmodel)s',
            'default': '%(dmodel)s',
            'default': '%(title)s',
            'regex': u'变速箱：(\S+)| ([手自]\S+)',
            'regex': [u'变速箱：(\S+)', '\s?([手自]\S+)'],
            'regex': u'([手自]{1,2}一?[动体])',
            'regex_fail': None,
            'regex_not': None,
            # 'processors': ['concat'],
        },
        'price': {
            'xpath': (
                text(cls('font_jiage')),
                text(cls('font46 color_ffffff font_weight')),
            ),
        },
        'price_bn': {
            'xpath': (
                text(id_('carInfo_price_xcsf', '/em')),
            ),
            'default': '%(description)s',
        },
        'brand_slug': {
            'xpath': (
                text(id_('carbrands')),
                # after_has(u'颜色'),
                has(u'品牌', '/span'),
            ),
            'default': '%(title)s',
        },
        'model_slug': {
            'xpath': (
                text(id_('carseriess')),
                text(cls('chexingpeizhi', '/a/../')),
                has(u'车型', '/span'),
            ),
            # 'processors': ['58.model_slug'],
            'default': '%(title)s',
        },
        'model_url': {
            'xpath': (
                href(id_('carseriess')),
            ),
            'format': True,
        },
        'dmodel': {
            'xpath': (
                text(id_('carlibs')),
                # text(cls('chexingpeizhi', '/a/../')),
            ),
            'default': '%(title)s',
            'regex': ur'(\d{2,4}款.+[版型])',
            # 'before': [u' 【', '['],
        },
        'city': {
            'xpath': (
                text(has_cls('address')),
                text(id_('curCity')),
                text(cls('breadCrumb f12', '/*[1]/a')),
                # '//meta[@name="location"]/@content',
            ),
            # 'processors': ['first', '58.city'],
            # 'regex': '\((\S+)\s\|',
            'regex': '\((\S+)[\)\s]',
            'before': '58',
            # 'regex': ['\((\S+)\s\|', '\((\S+)\\?'],
        },
        'contact': {
            'xpath': (
                # text(id_('carInfo_price_lxr')),
                text(id_('carInfo_price_lxr', u'/span[1]')),
                text(cls('lineheight_2', u'/span/a')),
                # has(u'二手车经理'),
                # after_has(u'联系', 'span[1]//text()'),
            ),
            # 'after': u'电话：',
            'after': u'：',
        },
        'region': {
            'xpath': (
                text(id_('address_detail')),
                has(u'址', '/span', '/p'), #地       址
            ),
        },
        'phone': {
            'xpath': (
                text(id_('t_phone')),
                text(id_('carInfo_price_lxr')),
                after_has(u'联系', 'span[1]//text()'),
            ),
            'processors': ['join', '58.phone'],
            # 'processors': ['concat'],
            'after': u'：',
        },
        'company_name': {
            'xpath': (
                text(cls('font_yccp')),
                # text(id_('jxs', '/')),
                has(u'商', '/a', '/p'), #经  销  商
            ),
        },
        'company_url': {
            'xpath': (
                href(cls('dianpu_link')),
                url(id_('jxs')),
            ),
            'format': True,
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
        'maintenance_record': {
            'xpath': (
                has(u'保养', '/span'),
                after_has(u'保养'),
            ),
        },
        'quality_service': {
            'xpath': (
                # text(id_('baozhang', '/')),
                text(cls('paddright13')),
                text(id_('carinfo_zb', '//' + has_cls('color_f47306'))),
                # text(id_('carinfo_zb', cls('font22 color_f47306 inline_block font_weight','','/'))),
                # has(u'延保'),
            ),
            'processors': ['join'],
        },
        'description': {
            'xpath': (
                text(with_cls('benchepeizhi', '/')),
                text(id_('carinfo_left', '/p')),
                # text(cls('font14 lineheight2 font_weight')),
            ),
            'processors': ['join'],
            'before': u'温馨提示',
        },
        'imgurls': {
            'xpath': (
                # img(id_('img1div')),
                attr(cls('mb_4'), 'src'),
                img(id_('carinfo_left')),

            ),
            'processors': ['join'],
        },
        'mandatory_insurance': {
            'xpath': (
                after_has(u'交强'),
                has(u'保险', '/span'),
            ),
        },
        # 'business_insurance': {
        #     'xpath': (
        #         u'//li/span[contains(text(), "商业险到期时间")]/../text()',
        #     ),
        # },
        'examine_insurance': {
            'xpath': (
                after_has(u'年检'),
                has(u'年检', '/span'),
            ),
        },
        # 'transfer_owner': {
        #     'xpath': (
        #         u'//li/span[contains(text(), "是否一手车")]/../text()',
        #     ),
        # },
        # 'car_application': {
        #     'xpath': (
        #         u'//li/span[contains(text(), "使用性质")]/../text()',
        #     ),
        # },
        # maintenance_desc
        'time': {
            'xpath': (
                text(id_('fbtime', '/span')),
                text(cls('time')),
            ),
        },
        'source_type': {
            'xpath': [
                # 厂商认证
                # 'boolean(//div[@class="rz_biaozhi"])',
                exists(cls('rz_biaozhi')),
                has(u'厂商认证'),
                exists(id_('carinfo_rzcl', '//' + has_cls('color_f47306'))),
                # exists(id_('carinfo_rzcl', cls('font22 color_f47306 inline_block font_weight','','/'))),
                # exists(id_('changshangrenzheng')),
                # 优质商家
                attr(has_id('icon_'), 'id'),
                # id_('icon_chengxincheshang'),
                # text(cls('paddright13')),
                # 普通商家
                href(cls('dianpu_link')),
                # '%(company_url)s',
                # 默认为 个人车
            ],
            # 'default': '%(company_url)s %(quality_service)s %(description)s',
            # 'default': '%(description)s %(quality_service)s %(company_url)s '.split(),
            'default': SOURCE_TYPE_GONGPINGJIA,
            'processors': ['58.source_type'],
        },
        'is_certifield_car': {
            # 'xpath': (
            #     # attr(has_id('icon_'), 'id'),
            #     # text(cls('paddright13')),
            #     exists(has_id('icon_')),
            # ),
            'default': False,
            # 'default': '%(quality_service)s %(description)s',
            'default': '%(quality_service)s',
            'default_fail': None,
            'default_fail': False,
            # 'processors': ['join', '58.is_certifield_car'],
        },
    },
}

parse_rule = {
    "url": {
        'xpath': (
            url('*[@id="infolist"]//*[@sortid="$sortId"]/'),
            url(cls('txt')),
            url(cls('t')),
            # '//div[@class="area-con01"]/ul[@class="arealist"]//div[@class="txt"]/a/@href',
        ),
        'contains': ['/ershouche/', 'shtml', 'infoid'],
        'format': True,
        "step": 'parse_detail',
    },
    "next_page_url": {
        "xpath": (
            '//dd[@class="dot"][1]/a[@href]/@href',
            url(cls('list-tabs')),
            '//a[@class="next"]/@href',
        ),
        'format': True,
        "step": 'parse',
        'max_pagenum': 25,
        # 'max_pagenum': 65,
        'incr_pageno': 5,
        'incr_pageno': 8,
    },
}

rule = {
    'name': u'58同城',
    'domain': '58.com',
    'base_url': 'http://quanguo.58.com',
    'base_url': 'no',
    # 'update': True,

    'start_urls': [
        # 'http://www.58.com/ershouche/changecity/',
        'http://cd.58.com/ershouche/',
        'http://bj.58.com/ershouche/',
        'http://nj.58.com/ershouche/',
        'http://sh.58.com/ershouche/',
        'http://quanguo.58.com/ershouche/',
        'http://volvo.58.com/ershouche/?sheng=quanguo&city=qg', # 尊沃
        'http://faw-vw.58.com/ershouche/', # 一汽大众
        'http://audi.58.com/ershouche/?sheng=quanguo&city=qg', # 奥迪品鉴
        'http://svwuc.58.com/ershouche/', # 上海大众
        'http://ghac.58.com/ershouche/?sheng=quanguo&city=qg', # 喜悦二手车、本田
        'http://chengxin.58.com/ershouche/?sheng=quanguo&city=qg', # 诚新二手车
        'http://yicheng.58.com/ershouche/?sheng=quanguo&city=qg', # 东风日产
        # 'http://quanguo.58.com/ershouche/0/',
        # 'http://quanguo.58.com/ershouche/1/',
        # 'http://quanguo.58.com/ershouche/?xbsx=1',
        # 'http://quanguo.58.com/ershouche/pn10/',
        # 'http://quanguo.58.com/ershouche/0/pn10/',
        # 'http://quanguo.58.com/ershouche/1/pn10/',
        # 'http://quanguo.58.com/ershouche/pn10/?xbsx=1',
        # 'http://bj.58.com/ershouche/21942816658953x.shtml', # 2
        # 'http://bj.58.com/ershouche/22531356944521x.shtml', # 2
        # 'http://bj.58.com/ershouche/22095630730144x.shtml', # 2
        # 'http://bj.58.com/ershouche/19417891266819x.shtml', # 5
        # 'http://sh.58.com/ershouche/21667174258462x.shtml', # 3
        # 'http://sy.58.com/ershouche/21851847601184x.shtml', # 4
        # 'http://cq.58.com/ershouche/22547675100938x.shtml', # control
        # 'http://cq.58.com/ershouche/22548469757449x.shtml', # volume
        # 'http://cq.58.com/ershouche/22548421513886x.shtml', # model_slug
        # 'http://nj.58.com/ershouche/22449972887201x.shtml', # 商家优质车
        # 'http://cd.58.com/ershouche/21975582547107x.shtml', # 厂商认证
        # 'http://cd.58.com/ershouche/22647994772126x.shtml', # 普通商家
        # 'http://bj.58.com/ershouche/22651418477321x.shtml', # 个人
        # 'http://cd.58.com/ershouche/22790753473060x.shtml',
        # 'http://faw-vw.58.com/detail/?infoid=22738356741918',
        # 'http://cd.58.com/ershouche/22790753473060x.shtml',
        # 'http://faw-vw.58.com/detail/?infoid=22704648710690',
        # 'http://faw-vw.58.com/detail/?infoid=22746478556964',
        # 'http://cq.58.com/ershouche/22738191832356x.shtml',
        # 'http://cd.58.com/ershouche/22449249479817x.shtml', # phone, region 5 -> icc
        # 'http://cq.58.com/ershouche/22505663203337x.shtml', # control city
        # 'http://bj.58.com/ershouche/22726563473184x.shtml', # bm -> model_url
        # 'http://bj.58.com/ershouche/22183591178656x.shtml', # city
        # 'http://cq.58.com/ershouche/22505663203337x.shtml', # city
        # 'http://mm.58.com/ershouche/22724556227465x.shtml', # control dmodel
        # 'http://su.58.com/ershouche/22124465115529x.shtml', # no month
        # 'http://cq.58.com/ershouche/22738191832356x.shtml', # no month
        # 'http://dg.58.com/ershouche/21896829745311x.shtml', #too much phone
        # 'http://yk.58.com/ershouche/22560359108383x.shtml',
        # 'http://zz.58.com/ershouche/22724266776481x.shtml',
        # 'http://bj.58.com/ershouche/22646499851428x.shtml',
        # 'http://sjz.58.com/ershouche/22779478418210x.shtml',
        # 'http://zz.58.com/ershouche/22679581563812x.shtml',
    ],

    'parse': parse_rule,

    'parse_detail': {
        "item": item_rule,
    }
}

fmt_rule_urls(rule)
# rule['parse'] = rule['parse_detail']
