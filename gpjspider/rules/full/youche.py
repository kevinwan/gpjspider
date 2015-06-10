# -*- coding: utf-8 -*-
from gpjspider.utils.constants import SOURCE_TYPE_SELLER
from utils import *


def new_requests(response, url_rule, spider):
    """
    function cityJump(cityid,std){
        setCookie("cityID",cityid,1,"");
        var url = 'http://www.youche.com/ershouche/w'+std;
        //window.location.href=url;
    }
    """
    _urls = response.xpath('//div[@class="f_r"]/li/a/@onclick').extract()
    urls = []
    base_url = 'http://www.youche.com/ershouche/w{0}/'
    num = 0
    for url in _urls:
        u = url.lower()
        s = u.find('cityjump(')
        if s < 0:
            return []
        s += len('cityjump(')
        e = u.index(',', s)
        city_id = u[s:e]
        std = u[e + 1]
        num += 1
        cookies = {'cityID': city_id, 'ccc': num}
        url_dict = {'url': base_url.format(std), 'cookies': cookies}
        urls.append(url_dict)
        break
    spider.log(u'urls is: {0}'.format(urls))
    return urls


item_rule = {
    "class": "UsedCarItem",
    "fields": {
        'title': {
            'xpath': (
                text(cls("carTitleInfo", "/h1")),
                #'//div[@class="carTitleInfo"]/h1/text()',
            ),
            'processors': ['first', 'strip'],
            'required': True,
        },
        'meta': {
            'xpath': (
                '//meta[@name="description" or @name="Description"]/@content',
            ),
            'processors': ['first', 'strip'],
        },
        'year': {
            'xpath': (
                text(cls("carTextList", "/span[1]")),
                #'//div[@class="carTextList"]/span[1]/text()',
            ),
            'processors': ['first', 'strip', 'year'],
        },
        'month': {
            'xpath': (
                text(cls("carTextList", "/span[1]")),
                #'//div[@class="carTextList"]/span[1]/text()',
            ),
            'processors': ['first', 'strip', 'month'],
        },
        'mile': {
            'xpath': (
                text(cls("carTextList", "/span[2]")),
                #'//div[@class="carTextList"]/span[2]/text()',
            ),
            'processors': ['first', 'strip', 'mile', 'decimal'],
        },
        'volume': {
            'xpath': (
                after_has(u"排量", "span", "span"),
                #u'//li/span[contains(text(), "排量")]/../span[@class="fr"]/text()',
            ),
            'processors': ['first', 'strip'],
        },

        'color': {
            'xpath': (
                after_has(u"颜色", "span", "span"),
                #u'//li/span[contains(text(), "颜色")]/../span[@class="fr"]/text()',
            ),
            'processors': ['first', 'strip'],
        },
        'control': {
            'xpath': (
                text(cls("carTextList", "/span[4]")),
                #'//div[@class="carTextList"]/span[4]/text()',
            ),
            'processors': ['first', 'strip'],
        },
        'price': {
            'xpath': (
                text(cls("nowPrice", "/b[@class='b0']")),
                u"//b[contains(text(), '厂家指导价')]/../../td[2]/text()",
                #'//div[@class="nowPrice"]/b[@class="b0"]/text()',
            ),
            'processors': ['first', 'strip', 'price', 'decimal'],
        },
        'price_bn': {
            'xpath': (
                text(cls("oldPrice", "/span[@class='sp01']/s")),
                #'//div[@class="oldPrice"]/span[@class="sp01"]/s/text()',
            ),
            'regex': u"(\d+\.\d+)",
            'processors': ['first', 'strip', 'decimal'],
        },
        'brand_slug': {
            'xpath': (
                after_has(u"品牌", "span[@class='fr']/a", "span"),
                # u'//li/span[contains(text(), "品牌")]/../span[@class="fr"]/a/text()',
            ),
            'processors': ['first', 'strip'],
        },
        'model_slug': {
            'xpath': (
                after_has(u"车系", "span[@class='fr']/a", "span"),
                # u'//li/span[contains(text(), "车系")]/../span[@class="fr"]/a/text()',
            ),
            'processors': ['first', 'strip'],
        },
        'city': {
            'xpath': (
                after_has(u"归属地", "span", "span"),
                # u'//li/span[contains(text(), "归属地")]/../span[@class="fr"]/text()',
            ),
            'processors': ['first', 'strip'],
        },
        'description': {
            'xpath': (
                text(cls("highlightsEidter", "/div[@class='txt']")),
                text(cls("ccInfoText", "/div[@class='areaText']")),
                # '//div[@class="highlightsEidter"]/div[@class="txt"]/text()',
                # '//div[@class="ccInfoText"]/div[@class="areaText"]/text()[1]',
            ),
            'processors': ['join', 'strip'],
        },
        'imgurls': {
            'xpath': (
                img(cls("phoneList", "/a/img")),
                '//div[@class="phoneList"]/a/img/@src',
            ),
            'processors': ['join', 'strip_imgurls'],
        },
        'mandatory_insurance': {
            'xpath': (
                after_has(u"年检", "span", "span"),
                #u'//li/span[contains(text(), "年检")]/../span[@class="fr"]/text()',
            ),
            'processors': [
                'first', 'strip', 'youche.examine_insurance'
            ],
        },
        # 'business_insurance': {
        # 'json': '-data$#$-cr$#$-procedureInfo$#$-crCommercialInsurance',
        # 'processors': ['strip'],  # 处理器
        # },
        'examine_insurance': {
            'xpath': (
                after_has(u"交强", "span", "span"),
                #u'//li/span[contains(text(), "交强")]/../span[@class="fr"]/text()',
            ),
            # 处理器
            'processors': ['first', 'strip', 'youche.examine_insurance'],
        },
        'transfer_owner': {
            'xpath': (
                after_has(u"过户次数", "span", "span"),
                #u'//li/span[contains(text(), "过户次数")]/../span[@class="fr"]/text()',
            ),
            'processors': ['first', 'strip', 'youche.transfer_owner'],
        },
        'condition_level': {
            'xpath': (
                after_has(u"车况", "span", "span"),
                #u'//li/span[contains(text(), "车况")]/../span[@class="fr cup"]/text()',
            ),
            'processors': ['first', 'strip'],
        },
        'maintenance_record': {
            'xpath': (
                u'boolean(//ul[@class="ccInfoCarList"]/li[contains(text(), "保养记录")]/span[contains(text(), "已查")])',
                u'boolean(//ul[@class="ccInfoCarList"]/li[contains(text(), "维修记录")]/span[contains(text(), "已查")])',
            ),
            'processors': ['youche.maintenance_record'],
        },
        'phone': {
            'xpath': (
                text(id_("linksCallTel")),
                '//*[@id="linksCallTel"]/text()',
            ),
            'processors': ['first', 'strip'],
        },
        # 'contact': {
        # 'default': u'优车诚品客服',
        #},
        #'company_name': {
        #    'default': u'优车诚品',
        #},
        #'company_url': {
        #    'default': 'http://www.youche.com/',
        #},

        # 'driving_license': {
        # 'json': '-data$#$-cr$#$-procedureInfo$#$-crDrivingLicense',
        # 'processors': ['strip'],  # 处理器
        # },
        # 'invoice': {
        # 'json': '-data$#$-cr$#$-procedureInfo$#$-crBuyCarInvoice',
        # 'processors': ['strip'],  # 处理器
        # },
        'quality_service': {
            'xpath': (
                text(cls("f13")),
                text(id_("rService", "/ul/li/a/div/div/p[@class='f13'']")),
                #'//*[@id="rService"]/ul/li/a/div/div/p[@class="f13"]/text()',
            ),
            'processors': ['join'],
        },
        'source_type': {
            'default': SOURCE_TYPE_SELLER,
        },
    },
}

parse_rule = {
    "url": {
        "xpath": (
            '//ul[@class="ulConListPro"]/li/div/a/@href',
        ),
        "step": 'parse_detail',
        'update': True,
        'category': 'usedcar'
    },
    "next_page_url": {
        "xpath": (
            u'//a[text()="下一页"]/@href',
        ),
        "excluded": ('javascript',),
        "format": "http://www.youche.com{0}",
        "step": 'parse',
        'incr_pageno': 1,
    },
}

rule = {
    # ==========================================================================
    # 基本配置
    #==========================================================================
    'name': u'优车诚品',
    'domain': 'youche.com',
    # start_urls  或者 start_url_template只能设置其一，
    # start_url_function 配合 start_url_template一起用
    #  start_url_function 必须返回一个生成器
    'start_urls': [
        'http://www.youche.com/ershouche/',
        #'http://www.youche.com/',
        # 'http://www.youche.com/detail/9719.shtml',
    ],

    #==========================================================================
    #  默认步骤  parse
    #==========================================================================
    # 'parse': {
    #     "url": {
    #         "function": new_requests,
    #         "step": 'parse_list',
    #     },
    # },
    #==========================================================================
    #  列表页步骤  parse_list
    #==========================================================================
    #'parse_list': {
    'parse': parse_rule,
    #==========================================================================
    #  详情页步骤  parse_detail
    #==========================================================================
    'parse_detail': {
        "item": item_rule
    },
}
