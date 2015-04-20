# -*- coding: utf-8 -*-
"""
优车诚品二手车
"""
from gpjspider.utils.constants import SOURCE_TYPE_SELLER


def pagenum_function(url):
    """
    http://www.youche.com/ershouche/p2
    """
    s = 'ershouche/p'
    if s not in url:
        return 1
    else:
        idx = url.strip(' /').find(s)
        return int(url[idx+len(s)])


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
        std = u[e+1]
        num += 1
        cookies = {'cityID': city_id, 'ccc': num}
        url_dict = {'url': base_url.format(std), 'cookies': cookies}
        urls.append(url_dict)
    spider.log(u'urls is: {0}'.format(urls))
    return urls


rule = {
    #==========================================================================
    #  基本配置
    #==========================================================================
    'name': u'优质二手车-优车诚品-增量更新规则',
    'domain': 'youche.com',
    # start_urls  或者 start_url_template只能设置其一，
    # start_url_function 配合 start_url_template一起用
    #  start_url_function 必须返回一个生成器
    'start_urls': ['http://www.youche.com/'],

    #==========================================================================
    #  默认步骤  parse
    #==========================================================================
    'parse': {
        "url": {
            "function": new_requests,
            # 新 url 对应的解析函数
            "step": 'parse_list',
            'dont_filter': True,
        },
    },
    #==========================================================================
    #  列表页步骤  parse_list
    #==========================================================================
    'parse_list': {
        "url": {
            "xpath": (
                '//ul[@class="ulConListPro"]/li/div/a/@href',
            ),
            'dont_filter': False,   # 默认值就是 False
            "step": 'parse_detail',
        },
        "incr_page_url": {
            "xpath": (u'//a[text()="下一页"]/@href',),
            "excluded": ('javascript'),
            "format": "http://www.youche.com{0}",
            'dont_filter': True,
            'pagenum_function': pagenum_function,
            'max_pagenum': 2,  # 增量爬取最大页号
            "step": 'parse_list',
        },
    },
    #==========================================================================
    #  详情页步骤  parse_detail
    #==========================================================================
    'parse_detail': {
        "item": {
            "class": "UsedCarItem",
            "fields": {
                'title': {
                    'xpath': ('//div[@class="carTitleInfo"]/h1/text()',),
                    'processors': ['first', 'strip'],
                    'required': True,
                },
                'meta': {
                    'xpath': (
                        '//meta[@name="description"]/@content',
                        '//meta[@name="Description"]/@content'
                    ),
                    'processors': ['first', 'strip'],
                },
                'year': {
                    'xpath': ('//div[@class="carTextList"]/span[1]/text()',),
                    'processors': ['first', 'strip'],
                },
                'month': {
                    'xpath': ('//div[@class="carTextList"]/span[1]/text()',),
                    'processors': ['first', 'strip'],
                },
                'mile': {
                    'xpath': ('//div[@class="carTextList"]/span[2]/text()',),
                    'processors': ['first', 'strip', 'mile', 'decimal'],
                },
                'volume': {
                    'xpath': (
                        u'//li/span[contains(text(), "排量")]/../span[@class="fr"]/text()',
                    ),
                    'processors': ['first', 'strip'],
                },

                'color': {
                    'xpath': (
                        u'//li/span[contains(text(), "颜色")]/../span[@class="fr"]/text()',
                    ),
                    'processors': ['first', 'strip'],
                },
                'control': {
                    'xpath': ('//div[@class="carTextList"]/span[4]/text()',),
                    'processors': ['first', 'strip'],
                },
                'price': {
                    'xpath': (
                        '//div[@class="nowPrice"]/b[@class="b0"]/text()',
                    ),
                    'processors': ['first', 'strip', 'decimal'],
                },
                'price_bn': {
                    'xpath': (
                        '//div[@class="oldPrice"]/span[@class="sp01"]/s/text()',
                    ),
                    'processors': ['first', 'strip', 'price', 'decimal'],
                },
                'brand_slug': {
                    'xpath': (
                        u'//li/span[contains(text(), "品牌")]/../span[@class="fr"]/a/text()',
                    ),
                    'processors': ['first', 'strip'],
                },
                'model_slug': {
                    'xpath': (
                        u'//li/span[contains(text(), "车系")]/../span[@class="fr"]/a/text()',
                    ),
                    'processors': ['first', 'strip'],
                },
                'city': {
                    'xpath': (
                        u'//li/span[contains(text(), "归属地")]/../span[@class="fr"]/text()',
                    ),
                    'processors': ['first', 'strip'],
                },
                'description': {
                    'xpath': (
                        '//div[@class="highlightsEidter"]/div[@class="txt"]/text()',
                        '//div[@class="ccInfoText"]/div[@class="areaText"]/text()[1]',
                    ),
                    'processors': ['join', 'strip'],
                },
                'imgurls': {
                    'xpath': ('//div[@class="phoneList"]/a/img/@src',),
                    'processors': ['join', 'strip_imgurls'],
                },
                'mandatory_insurance': {
                    'xpath': (
                        u'//li/span[contains(text(), "年检")]/../span[@class="fr cup"]/text()',
                    ),
                    'processors': ['first', 'strip'],  # 处理器
                },
                # 'business_insurance': {
                #     'json': '-data$#$-cr$#$-procedureInfo$#$-crCommercialInsurance',
                #     'processors': ['strip'],  # 处理器
                # },
                'examine_insurance': {
                    'xpath': (
                        u'//li/span[contains(text(), "交强")]/../span[@class="fr"]/text()',
                    ),
                    'processors': ['first', 'strip'],  # 处理器
                },
                'transfer_owner': {
                    'xpath': (
                        u'//li/span[contains(text(), "过户次数")]/../span[@class="fr"]/text()',
                    ),
                    'processors': ['first', 'strip', 'youche.transfer_owner'],
                },
                'condition_level': {
                    'xpath': (
                        u'//li/span[contains(text(), "车况")]/../span[@class="fr cup"]/text()',
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
                    'xpath': ('//*[@id="linksCallTel"]/text()',),
                    'processors': ['first', 'strip'],
                },
                'contact': {
                    'default': u'优车诚品客服',
                },
                'company_name': {
                    'default': u'优车诚品',
                },
                'company_url': {
                    'default': 'http://www.youche.com/',
                },

                # 'driving_license': {
                #     'json': '-data$#$-cr$#$-procedureInfo$#$-crDrivingLicense',
                #     'processors': ['strip'],  # 处理器
                # },
                # 'invoice': {
                #     'json': '-data$#$-cr$#$-procedureInfo$#$-crBuyCarInvoice',
                #     'processors': ['strip'],  # 处理器
                # },
                'quality_service': {
                    'xpath': (
                        '//*[@id="rService"]/ul/li/a/div/div/p[@class="f13"]/text()',
                    ),
                    'processors': ['join'],
                },
                'source_type': {
                    'default': SOURCE_TYPE_SELLER,
                },
            },
        },
    },
}
