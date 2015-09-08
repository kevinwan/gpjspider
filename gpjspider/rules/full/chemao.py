# -*- coding: utf-8 -*-
from .utils import *

item_rule = {
    "class": "UsedCarItem",
    "fields": {
        'title': {
            'xpath': (
                text(has_cls("accred-title", "//span[@class='title']")),
                text(id_('det_title')),
            ),
            'required': True,
        },
        'dmodel': {
            # 'xpath': (
            # ),
            'default': '%(title)s',
            'regex': u'\d{4}年款.*',
        },
        'meta': {
            'xpath': (
                '//meta[@name="description" or @name="Description"]/@content',
            ),
            'regex': u'(.*)_车猫',
        },
        'year': {
            'xpath': (
                before_has(u'上牌时间'),
                text(has_cls('car_detail', '/div[1]/em')),
            ),
        },
        'month': {
            'xpath': (
                before_has(u'上牌时间'),
                text(has_cls('car_detail', '/div[1]/em')),
            ),
        },
        'mile': {
            'xpath': (
                text(has_cls('car_detail', '/div[2]/em')),
                before_has(u'行驶里程', 'span'),
            ),
            'processors': ['first', 'chemao.mile']
        },
        'volume': {
            'xpath': (
                text(has_cls('basic-config', u'//td[contains(text(), "发   动  机：")]')),
            ),
            'default': '%(title)s',
            'regex': u'\d\.\dL',
        },
        'phone': {
            'xpath': (
                attr(id_('cert-contact'), 'data-car_id'),
                attr(id_('car_id'), 'value'),
            ),
            'processors': ['first', 'chemao.phone'],
        },
        'color': {
            'xpath': (
                after_has(u"颜色", 'td', prefix='//td'),
            ),
        },
        'control': {
            'xpath': (
                text(has_cls('basic-config', u'//td[contains(text(), "变   速  器：")]')),
                after_has(u'变速箱', 'td'),
                after_has(u'变速箱类型', 'td'),
            ),
            'regex': u'变   速  器：(.*)',
        },
        'region': {
            'xpath': (
                text(has_cls('view-places', '/p')),
                after_has(u'车源地', 'td'),
                text(has_cls('address-text', '/p[3]')),
            ),
            'processors': ['first', 'chemao.region']
        },
        'contact': {
            'xpath': (
                text(has_cls('view-places', '/p')),
                text(has_cls('address-text', '/p[2]')),
            ),
            'regex': u'商家信息：([^，]*)，?.*'
        },
        'price': {
            'xpath': (
                text(has_cls('accred-price', '/span')),
                text(has_cls('price-info', '/span[4]/b')),
                text(has_cls('carPrice', '/span')),
                after_has(u'车主报价'),
            ),
        },
        'price_bn': {
            'xpath': (
                text(has_cls('accred-price', '/del')),
                has(u'新车价：', prefix='//p'),
                has(u'新车价(含购置税)', prefix='//p'),
            ),
            'regex': '：(.*)',
        },
        'brand_slug': {
            # 'xpath': (
            #
            # ),
            'default': '%(title)s',
            'regex': '(.*)\s?\d{4}.*',
        },
        'model_slug': {
            'xpath': (
                text(cls('show-breadcrumb', '//ul/li[4]/a')),
            ),
            'default': '%(dmodel)s',
            'processors': ['strip', 'first', 'chemao.model_slug'],
        },
        'model_url': {
            'xpath': (
                href(cls('show-breadcrumb', '//ul/li[4]/a')),
            ),
            'processors': ['first', 'chemao.model_url'],
        },
        'city': {
            'xpath': (
                '//meta[@name="location"]/@content',
                before_has(u'车源地'),
                text(has_cls('car_detail', '/div[3]/em')),
            ),
            'regex': u'city=(.*);'
        },
        'description': {
            'xpath': [
                has(u'检车评语', '/../text()'),
                has(u'车型优势', '/../text()'),
                has(u'当前车况', '/../text()'),
                has(u'车猫建议', '/../text()'),
                after_has(u'车主描述'),
            ],
            'processors': ['join'],
        },
        'imgurls': {
            'xpath': (
                img(cls("thumbnail-info", "/ul/li/a")),
                img(cls("car-photo")),
            ),
            'processors': ['join'],
        },
        'mandatory_insurance': {
            'xpath': (
                after_has(u'交强险到期', 'td'),
            ),
        },
        'business_insurance': {
            'xpath': (
                after_has(u'商险到期', 'td'),
            ),
            'processors': ['first', 'strip', 'chemao.business_insurance']
        },
        'company_name': {
            'xpath': (
                text(has_cls('view-places', '/p')),
                text(has_cls('address-text', '/p[2]')),
            ),
            'regex': u'商家信息：([^，]*)，?.*'
        },
        # 'company_url': {
        #     'xpath': (
        #         url(cls("newcompany")),
        #     ),
        #     'format': True,
        # },
        'examine_insurance': {
            'xpath': (
                after_has(u'年检有效'),
            ),
        },
        'transfer_owner': {
            'xpath': (
                after_has(u'是否是一手车'),
            ),
            'processors': ['first', 'chemao.transfer_owner']
        },
        'car_application': {
            'xpath': (
                after_has(u'使用性质'),
            ),
        },
        'maintenance_desc': {
            'xpath': (
                after_has(u'保养情况'),
            ),
        },
        'time': {
            'xpath': (
                text(has_cls('release-time')),
                has(u'发布时间：'),
            ),
            'regex': u'：(.*)',
        },
        'is_certifield_car': {
            'xpath': (
                exists(has_cls('cert')),
            ),
        },
        'source_type': {
            # 'xpath': (
            #
            # ),
            'default': '%(is_certifield_car)s',
            'processors': ['chemao.source_type'],
        },
        'quality_service': {
            'xpath': (
                text(cls('service-tags', '//a')),
            ),
            'default': u'车辆合法，绝无火烧、水淹',
            'processors': ['chemao.quality_service'],
        },
        'status': {
            'xpath': (
                u'//div[@class="events_mark04"]/img',
                u'//div[@class="car-status"]/img',
            ),
            'processors': ['first', 'chemao.status'],
            'default': 'Y',
        },
    },
}

list_rule = {
    "url": {
        "xpath": (
            url(has_cls('carPicList', '//div[contains(@class, "pic")]')),
        ),
        "format": True,
        'contains': '/show-id',
        "step": 'parse_detail',
    },
    "next_page_url": {
        "xpath": (
            '//a[@class="page-next"]/@href',
        ),
        "format": 'http://www.chemao.com.cn/{0}',
        "step": 'parse',
    },
}

rule = {
    'name': u'车猫',
    'domain': 'chemao.com.cn',
    'start_urls': [
        # 'http://www.chemao.com.cn/market-condition-QLJIXTnPB9lZ6cCEX9C4WtZZlgytXtsdRywDW96LPeC8i9PShxdo0qNdI0GodJdKzeK-cZlXn4tCesaXbhGiYg...html',
        # 'http://www.chemao.com.cn/market-condition-UWVvSj7RiYGjvVwyjPLw8cnAMWlKmLNcHabhqnZUgKSkwAvgp9TvjzQE-5xIVlHmugSstOdlIfsjWeDh0IclLTB6cEAJ0bcBbT9ofI6UKwZ3b1nrl5ZmkRG6XmrKkpar.html',
        'http://www.chemao.com.cn/s/00so10',
        'http://www.chemao.com.cn/s/00so10cf1',
        # 'http://www.chemao.com.cn/market-condition-QLJIXTnPB9lZ6cCEX9C4WtZZlgytXtsdRywDW96LPeC8i9PShxdo0qNdI0GodJdKzeK-cZlXn4tCesaXbhGiYg..-page-46.html',
        # 'http://www.chemao.com.cn/market-condition-UWVvSj7RiYGjvVwyjPLw8cnAMWlKmLNcHabhqnZUgKSkwAvgp9TvjzQE-5xIVlHmugSstOdlIfsjWeDh0IclLTB6cEAJ0bcBbT9ofI6UKwZ3b1nrl5ZmkRG6XmrKkpar-page-46.html',
        # 'http://www.chemao.com.cn/market-condition-_XN6-BeggGcgdmcHLRh4_7j_IpkRh9RwR6I61UZlyIE..html',
        #'http://www.chemao.com.cn/market.html', # 默认会取请求所在城市的数据
        # 'http://www.chemao.com.cn/show-id-1153094.html',  # 认证车
        # 'http://www.chemao.com.cn/show-id-1138467.html',  # 非认证车
        # 'http://www.chemao.com.cn/show-id-1156880.html',  # 非认证车
        # 'http://www.chemao.com.cn/show-id-1158143.html',
        # 'http://www.chemao.com.cn/show-id-1167631.html',   # 非认证车
        # 'http://www.chemao.com.cn/show-id-1194012.html',   # 非认证车
        # 'http://www.chemao.com.cn/show-id-1193806.html',
        # 'http://www.chemao.com.cn/show-id-1194586.html',
        # 'http://www.chemao.com.cn/show-id-1196508.html',
        # 'http://www.chemao.com.cn/show-id-1194395.html',
        # 'http://www.chemao.com.cn/show-id-1201725.html',
        # 'http://www.chemao.com.cn/show-id-1205154.html',  # phone "4001666556转18853"
        # 'http://www.chemao.com.cn/show-id-1210154.html',  # offline
        # 'http://www.chemao.com.cn/show-id-1210132.html',  # offline
        # 'http://www.chemao.com.cn/show-id-1153094.html',  # offline
    ],
    'base_url': 'http://www.chemao.com.cn',
    'per_page': 21,
    'pages': 100,

    'parse': list_rule,

    'parse_detail': {
        "item": item_rule,
        "replace": ({'encoding': 'gbk'},)
    }
}

fmt_rule_urls(rule)
# rule['parse'] = rule['parse_detail']
