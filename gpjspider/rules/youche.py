# -*- coding: utf-8 -*-
"""
优车诚品二手车
"""


def excluded_func(url_str):
    """
    返回True表示 可用，否则表示不可用
    """
    return True


rule = {
    #==========================================================================
    #  基本配置
    #==========================================================================
    'name': u'优质二手车-优车诚品-规则',
    'domain': 'xin.com',
    # start_urls  或者 start_url_template只能设置其一，
    # start_url_function 配合 start_url_template一起用
    #  start_url_function 必须返回一个生成器
    'start_urls': ['http://www.youche.com/ershouche/'],

    #==========================================================================
    #  默认步骤  parse
    #==========================================================================
    'parse': {
        "url": {
            "xpath": (
                '//div[@class="box"]/ul[@class="ulCon"]/li/a[contains(@href, "javascript")]/@href',
                '//div[@class="box"]/ul[@class="ulCon"]/div/div/li/a[contains(@href, "javascript")]/@onclick'
            ),
            "excluded": excluded_func,
            "format": "http://www.xin.com{0}",
            # 新 url 对应的解析函数
            "step": 'parse_detail',
        }
    },
    #==========================================================================
    #  详情页步骤  parse_detail
    #==========================================================================
    'parse_detail': {
        "item": {
            "class": "UsedCarItem",
            "fields": {
                'title': {
                    'xpath': ('//div[@class="tit"]/h1/text()',),
                    'processors': ['strip'],  # 处理器
                    'required': True,   # 默认为 False
                },
                'meta': {
                    'xpath': ('//meta[@name="description"]/@content',),
                    'processors': ['strip'],  # 处理器
                },
                'year': {
                    'xpath': (u'//li[@class="br"]/span[contains(text(), "上牌时间")]/../em/text()',),
                    'processors': ['strip'],  # 处理器
                },
                'month': {
                    'xpath': (u'//li[@class="br"]/span[contains(text(), "上牌时间")]/../em/text()',),
                    'processors': ['strip'],  # 处理器
                },
                'mile': {
                    'xpath': (u'//li[@class="br"]/span[contains(text(), "行驶里程")]/../em/text()',),
                    'processors': ['strip'],  # 处理器
                },
                'volume': {
                    'xpath': (u'//li[@class="br"]/span[contains(text(), "排量")]/../em/text()',),
                    'processors': ['strip'],  # 处理器
                },

                'color': {
                    'xpath': (u'//td[contains(text(), "颜色")]/following-sibling::td/text()',),
                    'processors': ['strip'],  # 处理器
                },
                'control': {
                    'xpath': (u'//td[contains(text(), "变速箱")]/following-sibling::td/text()',),
                    'processors': ['strip'],  # 处理器
                },
                'price': {
                    'xpath': (u'//div[@class="wan_1"]/em/text()',),
                    'processors': ['strip'],  # 处理器
                },
                'price_bn': {
                    'xpath': (u'//div[@class="wan_2"]/span/del/text()',),
                    'processors': ['strip'],  # 处理器
                },
                'brand_slug': {
                    'xpath': ('//div[@class="tit"]/h1/text()',),
                    'processors': ['strip'],  # 处理器
                },
                'model_slug': {
                    'xpath': ('//div[@class="tit"]/h1/text()',),
                    'processors': ['strip'],  # 处理器
                },
                'city': {
                    'xpath': (u'//li/span[contains(text(), "销售城市")]/../em/text()',),
                    'processors': ['strip'],  # 处理器
                },
                'description': {
                    'xpath': (u'//div[@class="test-report"]/div[@class="test-txt"]/ul/li/text()',),
                    'processors': ['strip'],  # 处理器
                },
                'imgurls': {
                    'xpath': ('//div[@class="carimg"]/div/img/@src',),
                    'processors': ['strip'],  # 处理器
                },
                'mandatory_insurance': {
                    'xpath': (u'//td[contains(text(), "保险到期时间")]/following-sibling::td/text()',),
                    'processors': ['strip'],  # 处理器
                },
                # 'business_insurance': {
                #     'json': '-data$#$-cr$#$-procedureInfo$#$-crCommercialInsurance',
                #     'processors': ['strip'],  # 处理器
                # },
                'examine_insurance': {
                    'xpath': (u'//td[contains(text(), "年检有效期")]/following-sibling::td/text()',),
                    'processors': ['strip'],  # 处理器
                },
                'transfer_owner': {
                    'xpath': (u'//td[contains(text(), "过户次数")]/following-sibling::td/text()',),
                    'processors': ['strip'],  # 处理器
                },
                # 'driving_license': {
                #     'json': '-data$#$-cr$#$-procedureInfo$#$-crDrivingLicense',
                #     'processors': ['strip'],  # 处理器
                # },
                # 'invoice': {
                #     'json': '-data$#$-cr$#$-procedureInfo$#$-crBuyCarInvoice',
                #     'processors': ['strip'],  # 处理器
                # },
                # 'quality_service': {
                #     'default': u' '.join([
                #         u'268V专业检测',
                #         u'6个月免费质保',
                #         u'30天包退',
                #         u'安全交易服务',
                #     ])
                # },
            },
        },
    },
}
