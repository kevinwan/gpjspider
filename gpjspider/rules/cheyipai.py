# -*- coding: utf-8 -*-


def start_function(start_url_template, spider):
    """
    """
    pagesize = 50
    pageno = 1
    while pageno < 2:
        url = start_url_template.format(pageno=pageno, pagesize=pagesize)
        spider.log(u'start request:pageno:{0}, pagesize={1}'.format(
            pageno, pagesize)
        )
        yield url
        pageno += 1

rule = {
    #==========================================================================
    #  基本配置
    #==========================================================================
    'name': u'优质二手车-车易拍-规则',
    'domain': 'cheyipai.com',
    # start_urls  或者 start_url_template只能设置其一，
    # start_url_function 配合 start_url_template一起用
    #  start_url_function 必须返回一个生成器
    # 'start_urls': [],
    # 定义了pageno  和 pagesize
    'start_url_template': (
        'http://c.cheyipai.com/api/goods/goodsList'
        '?bparam=%7B%22sort%22%3A%22%22%2C%22regCity%22%3A'
        '%22%22%2C%22page%22%3A{pageno}%2C%22pageSize%22%3A{pagesize}%7D'),
    'start_url_function': start_function,

    #==========================================================================
    #  默认步骤  parse
    #==========================================================================
    'parse': {
        "url": {
            "json": '-data$#$|ALL$#$-goodsId',
            # 要排除的 url
            "excluded": [
                "xxxxx",
            ],
            # 将 ID 填充进去
            "format": ("http://c.cheyipai.com/api/goods/goodsDetail?bparam"
                       "=%7B%22id%22%3A%22{0}%22%7D"),
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
                    'json': '-data$#$-goodsName',
                    'processors': ['strip'],  # 处理器
                    'required': True,   # 默认为 False
                },
                # 'meta': {
                #     'xpath': ('//meta[@name="description"]/@content',),
                #     'processors': ['strip'],  # 处理器
                # },
                'year': {
                    'json': '-data$#$-goodsRegyear',
                    'processors': ['strip', 'cheyipai.year'],  # 处理器
                },
                'month': {
                    'json': '-data$#$-goodsRegyear',
                    'processors': ['strip', 'cheyipai.month'],  # 处理器
                },
                'time': {
                    'json': '-data$#$-goodsOlinedate',
                    'processors': ['strip'],  # 处理器
                },
                'mile': {
                    'json': '-data$#$-goodsMileage',
                    'processors': ['strip'],  # 处理器
                },
                'volume': {
                    'json': '-data$#$-cr$#$-configInfo$#$-crVolumn',
                    'processors': ['strip'],  # 处理器
                },

                'color': {
                    'json': '-data$#$-goodsCarcolor',
                    'processors': ['strip'],  # 处理器
                },
                'control': {
                    'json': '-data$#$-cr$#$-configInfo$#$-crTransForm',
                    'processors': ['strip'],  # 处理器
                },
                'price': {
                    'json': '-data$#$-goodsPrice',
                    'processors': ['strip', 'float'],  # 处理器
                },
                'price_bn': {
                    'json': '-data$#$-newCarPrice',
                    'processors': ['strip', 'float'],  # 处理器
                },
                'brand_slug': {
                    'json': '-data$#$-brandName',
                    'processors': ['strip'],  # 处理器
                },
                'model_slug': {
                    'json': '-data$#$-seriaName',
                    'processors': ['strip'],  # 处理器
                },
                'city': {
                    'json': '-data$#$-goodsReglocation',
                    'processors': ['strip'],  # 处理器
                },
                'description': {
                    'json': '-data$#$-goodsFeatureDesc',
                    'processors': ['strip'],  # 处理器
                },
                'imgurls': {
                    'json': '-data$#$-goodsImages',
                    'processors': ['strip'],  # 处理器
                },
                'mandatory_insurance': {
                    'json': '-data$#$-cr$#$-procedureInfo$#$-crValid',
                    'processors': ['strip'],  # 处理器
                },
                'business_insurance': {
                    'json': '-data$#$-cr$#$-procedureInfo$#$-crCommercialInsurance',
                    'processors': ['strip'],  # 处理器
                },
                'examine_insurance': {
                    'json': '-data$#$-cr$#$-procedureInfo$#$-crAnnualPeriodValidity',
                    'processors': ['strip'],  # 处理器
                },
                'transfer_owner': {
                    'json': '-data$#$-cr$#$-transInfo$#$-crTransCount',
                    'processors': ['strip', 'int'],  # 处理器
                    'default': 0
                },
                'driving_license': {
                    'json': '-data$#$-cr$#$-procedureInfo$#$-crDrivingLicense',
                    'processors': ['strip'],  # 处理器
                },
                'invoice': {
                    'json': '-data$#$-cr$#$-procedureInfo$#$-crBuyCarInvoice',
                    'processors': ['strip'],  # 处理器
                },
                'quality_service': {
                    'default': u' '.join([
                        u'268V专业检测',
                        u'6个月免费质保',
                        u'30天包退',
                        u'安全交易服务',
                    ])
                },
            },
        },
    },
}
