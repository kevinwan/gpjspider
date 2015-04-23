# -*- coding: utf-8 -*-
from gpjspider.utils.constants import SOURCE_TYPE_SELLER


def start_function(start_url_template, spider):
    """
    """
    pagesize = 50
    pageno = 1
    while pageno < 100:
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
    'domain': 'c.cheyipai.com',
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
            "excluded": [
                "xxxxx",
            ],
            "format": ("http://c.cheyipai.com/api/goods/goodsDetail?bparam"
                       "=%7B%22id%22%3A%22{0}%22%7D"),
            "step": 'parse_detail',
            'update': True,
            'category': 'usedcar'
        }
    },
    #==========================================================================
    #  详情页步骤  parse_detail
    #==========================================================================
    'parse_detail': {
        "item": {
            'real_url': "http://c.cheyipai.com/car_detail.jsp?goodsid={0}",
            "class": "UsedCarItem",
            "fields": {
                'url': {
                    'function': {
                        'name': 'cheyipai_url',
                    },
                },
                'title': {
                    'json': '-data$#$-goodsName',
                    'processors': ['strip'],
                    'required': True,
                },
                'year': {
                    'json': '-data$#$-goodsRegyear',
                    'processors': ['strip', 'cheyipai.year'],
                },
                'month': {
                    'json': '-data$#$-goodsRegyear',
                    'processors': ['strip', 'cheyipai.month'],
                },
                'time': {
                    'json': '-data$#$-goodsOlinedate',
                    'processors': ['strip'],
                },
                'mile': {
                    'json': '-data$#$-goodsMileage',
                    'processors': ['strip'],
                },
                'volume': {
                    'json': '-data$#$-cr$#$-configInfo$#$-crVolumn',
                    'processors': ['strip'],
                },

                'color': {
                    'json': '-data$#$-goodsCarcolor',
                    'processors': ['strip'],
                },
                'control': {
                    'json': '-data$#$-cr$#$-configInfo$#$-crTransForm',
                    'processors': ['strip'],
                },
                'price': {
                    'json': '-data$#$-goodsPrice',
                    'processors': ['strip', 'gpjfloat'],
                },
                'price_bn': {
                    'json': '-data$#$-newCarPrice',
                    'processors': ['strip', 'gpjfloat'],
                },
                'brand_slug': {
                    'json': '-data$#$-brandName',
                    'processors': ['strip'],
                },
                'model_slug': {
                    'json': '-data$#$-seriaName',
                    'processors': ['strip'],
                },
                'city': {
                    'json': '-data$#$-goodsReglocation',
                    'processors': ['strip'],
                },
                'description': {
                    'json': '-data$#$-goodsFeatureDesc',
                    'processors': ['strip'],
                },
                'imgurls': {
                    'json': '-data$#$-goodsImages',
                    'processors': ['strip', 'cheyipai.imgurls'],
                },
                'mandatory_insurance': {
                    'json': '-data$#$-cr$#$-procedureInfo$#$-crValid',
                    'processors': ['strip'],
                },
                'business_insurance': {
                    'json': '-data$#$-cr$#$-procedureInfo$#$-crCommercialInsurance',
                    'processors': ['strip'],
                },
                'examine_insurance': {
                    'json': '-data$#$-cr$#$-procedureInfo$#$-crAnnualPeriodValidity',
                    'processors': ['strip'],
                },
                'transfer_owner': {
                    'json': '-data$#$-cr$#$-transInfo$#$-crTransCount',
                    'processors': ['strip', 'gpjint'],
                    'default': 0
                },
                'driving_license': {
                    'json': '-data$#$-cr$#$-procedureInfo$#$-crDrivingLicense',
                    'processors': ['strip'],
                },
                'invoice': {
                    'json': '-data$#$-cr$#$-procedureInfo$#$-crBuyCarInvoice',
                    'processors': ['strip'],
                },
                'quality_service': {
                    'default': u' '.join([
                        u'6个月免费质保',
                        u'30天包退',
                    ])
                },
                'source_type': {
                    'default': SOURCE_TYPE_SELLER,
                },
                'meta': {
                    'default': (
                        u'车易拍是中国领先二手车在线交易平台，采用国家认证的268V标准化二手'
                        u'车评估系统，保证车源真实可靠，交易安全省心。买车卖车就在车易拍。'
                    )
                },
                'contact': {
                    'default': u'车易拍客服'
                },
                'phone': {
                    'default': u'4000690555'
                },
                'company_name': {
                    'default': u'车易拍'
                },
                'company_url': {
                    'default': u'http://c.cheyipai.com/'
                },
                'is_certifield_car': {
                    'default': True
                },

            },
        },
    },
}
