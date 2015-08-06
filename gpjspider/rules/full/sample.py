# -*- coding: utf-8 -*-
from .utils import *

item_rule = {
    "class": "UsedCarItem",
    "fields": {
        # 1. 所有字段都以实际页面的灵活处理，原则是完整、精准和兼容/健壮！！
        # 2. 字段类型不要混淆，缺省时也要注意
        # 3. 数据结果要准确，不要有类型错误/多余的信息
        # 4. url字段的地址要完整
        # 5. 凡有的字段都加在规则中，不要漏失，没有的可以注释掉。。
        # 6. 遇到特殊规需处理，如果是通用性的就在公共代码上更新（添加相应的测试）；
        # 否则私有化处理。避免影响其他地方的正常运行
        # OPT as follow:
        # a 避免标点    b 保持格式的统一与整洁
        # c smart tricks instead of more codes
        # d less processors

        'title': {
            'xpath': (
                text(cls('h1')),
            ),
            # 标题是车源页的标识*, 没有的一律不解析item
            # 现阶段这样处理，后面不排除有特殊情况
            'required': True,
        },
        'dmodel': {
            # 网站自己的车型，若没有则取
            # 含年款在内的有效信息，去掉无用内容！如下regex+before的处理
            'default': '%(title)s',
            # 'regex': u'(\S+\d{2,4}款.+)\s\d{4}年上牌',
            # 'before': '[',
        },
        'meta': {
            # 网页的元信息，很多SEO好点的网站都会把一些搜索的关键信息存放在这以便搜索引擎能收纳并高效查找。。
            # 这里可以提取不少的信息，当然优先还是以其他方式为主、meta备胎
            'xpath': (
                # d/D的这种小的区别可以放在一起打包处理
                '//meta[@name="description" or @name="Description"]/@content',
            ),
        },
        'year': {  # 年 YYYY 19/20** int
            'xpath': (
                after_has(u'上牌时间'),
            ),
        },
        'month': {  # 月 m 1-12 int
            'xpath': (
                # TODO: add support of format %(year)s
                after_has(u'上牌时间'),
            ),
        },
        'mile': {  # ？万公里
            'xpath': (
                after_has(u'行驶里程'),
            ),
        },
        'volume': {  # \d.\d 升(L/T)
            'xpath': (
                after_has(u'排量'),
            ),
            'default': '%(title)s',
        },
        'color': {  # 颜色描述：红、蓝色、深内饰。。
            'xpath': (
                after_has(u'颜色'),
            ),
        },
        'control': {  # 手动/自动/手自一体
            # 'xpath': (
            #     after_has(u'变速箱'),
            # ),
            'default': '%(dmodel)s',
            'regex': [u'变速箱：(\S+)', '\s?([手自]\S+)'],  # 多匹配
            'regex': u' ([手自]\S*[动体])',  # 唯一匹配
            'regex_fail': None,  # 匹配失败
            'regex_not': None,  # 匹配不上
        },
        'price': {  # 车主报价或车源的成交价
            'xpath': (
                text(cls('font_jiage')),
            ),
        },
        'price_bn': {  # 新车/厂商指导价，不含过户税之类的
            # xpath -> default 网页上没有专门信息的时候，可通过meta/desc
            'default': '%(description)s',
        },
        # visit http://pricebook.cn/user/model_match/ to validate brand & model info
        'brand_slug': {  # 网站自己的品牌
            'xpath': (
                text(id_('carbrands')),
            ),
            'default': '%(title)s',
        },
        'model_slug': {  # 网站自己的车系
            'xpath': (
                text(id_('carseriess')),
            ),
            'default': '%(title)s',
        },
        'model_url': {  # 网站自己的车系url, mush crawl if has
            'xpath': (
                href(id_('carseriess')),
            ),
            'format': True,
        },
        'city': {  # 车源归属地、所在城市
            'xpath': (
                '//meta[@name="location"]/@content',
            ),
            'processors': ['first', '58.city'],
        },
        'contact': {  # 联系人
            'xpath': (
                after_has(u'车主', 'span[1]//text()'),
            ),
        },
        'region': {  # 看车地点
            'xpath': (
                text(id_('address_detail')),
            ),
        },
        'phone': {  # 联系电话
            'xpath': (
                text(id_('t_phone', '/')),
            ),
            'processors': ['join'],
            'processors': ['concat'],
        },
        'company_name': {  # 商家名称
            'xpath': (
                text(cls('font_yccp')),
            ),
        },
        'company_url': {  # 商家地址
            'xpath': (
                url(cls('dianpu_link')),
            ),
        },
        # 行驶证、发票 有/无/齐全/..
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
        'maintenance_record': {  # 车辆是否保养: 保养记录 -> True/False
            'xpath': (
                after_has(u'保养'),
            ),
        },
        # maintenance_desc # 车辆保养记录描述
        # (有|无|全程|部分)?4S保养、不?齐全、有保养..
        # condition_level # 车况等级 123 > ABC > 优良
        # condition_detail # 车况介绍/检测报告
        'description': {  # 车源描述，酌情去掉无用信息
            'xpath': (
                text(with_cls('benchepeizhi', '/')),
            ),
            'processors': ['join'],
            'before': u'温馨提示：',
        },
        'imgurls': {  # 车源描述，酌情去掉无用信息
            'xpath': (
                # img(id_('img1div')),
                attr(cls('mb_4'), 'src'),
            ),
            'processors': ['join'],
        },
        # 交强险、商业险、年检 YYYY-MM-1，需处理过期/到期之类的情况
        'mandatory_insurance': {
            'xpath': (
                after_has(u'交强'),
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
            ),
        },
        # 'transfer_owner': {# 过户次数 int
        #     'xpath': (
        #         u'//li/span[contains(text(), "是否一手车")]/../text()',
        #     ),
        # },
        # 'car_application': {# 家用/非营运/..
        #     'xpath': (
        #         u'//li/span[contains(text(), "使用性质")]/../text()',
        #     ),
        # },
        'time': {  # 最真实的发布时间
            'xpath': (
                text(cls('time')),
            ),
        },
        'quality_service': {  # 质保服务, tag:
            # **包退/包换，**天/**公里保修，**质保/延保等等
            'xpath': (
                # text(id_('baozhang', '/')),
                text(cls('paddright13')),
                # has(u'质保'),
                # has(u'延保'),
            ),
            'processors': ['join'],
        },
        'is_certifield_car': {  # 是否优质车
            # 质保服务 -> 网站提供的类似区分 -> 网站平台所有的车源性质
            'xpath': (
                # attr(has_id('icon_'), 'id'),
                # text(cls('paddright13')),
                exists(has_id('icon_')),
            ),
            'default': '%(quality_service)s',
            'default_fail': None,
        },
        'source_type': {  # 来源类型
            # 1老爬虫 2优质车商 3品牌认证车商 4个人车源 5普通车商
            # 从入口爬取的所有类型要全部覆盖且能正确区分
            'xpath': [
                # 厂商认证
                exists(cls('rz_biaozhi')),
                # 优质商家
                attr(has_id('icon_'), 'id'),
                # 普通商家
                url(cls('dianpu_link')),
                # 默认为 个人车
            ],
            'default': '{item}', # offer item for processors to handle
            'processors': ['58.source_type'],
        },
        'status': {
            'xpath': (
                text(id_('sold_button')),
                text(cls('already-buy')),
            ),
            # 'processors': ['first', 'ygche.status'],
        },
    },
}

list_rule = {
    "url": {  # 车源详情链接
        'xpath': (
            url('*[@id="infolist"]//*[@sortid]/'),
        ),
        'contains': ['/ershouche/'],
        "step": 'parse_detail',  # 下一步解析车源详情信息
    },
    "next_page_url": {  # 车源列表翻页
        "xpath": (
            # url(cls('list-tabs')),
            '//a[@class="next"]/@href',
        ),
        'format': True,
        "step": 'parse',
        'max_pagenum': 25,  # 全量爬取的最大页数
        'incr_pageno': 8,  # 增量爬取的最大页数
    },
}

rule = {
    'name': u'58同城',
    'domain': '58.com',
    'base_url': 'http://quanguo.58.com',
    'per_page': 20,
    'pages': 100,
    # 'update': True,

    'start_urls': [
        'http://quanguo.58.com/ershouche/',
        'http://quanguo.58.com/ershouche/0/',
        'http://quanguo.58.com/ershouche/1/',
        'http://quanguo.58.com/ershouche/?xbsx=1',
        # 'http://quanguo.58.com/ershouche/pn15/',
        # 'http://quanguo.58.com/ershouche/0/pn15/',
        # 'http://quanguo.58.com/ershouche/1/pn15/',
        # 'http://quanguo.58.com/ershouche/pn15/?xbsx=1',
        # 'http://bj.58.com/ershouche/21942816658953x.shtml', # 2
        # 'http://bj.58.com/ershouche/22095630730144x.shtml', # 2
        # 'http://bj.58.com/ershouche/19417891266819x.shtml', # 2
        # 'http://sh.58.com/ershouche/21667174258462x.shtml', # 3
        # 'http://sy.58.com/ershouche/21851847601184x.shtml', # 4
    ],

    'parse': list_rule,

    'parse_detail': {
        "item": item_rule,
    }
}

fmt_rule_urls(rule)
# 本地测试详情页面用
# rule['parse'] = rule['parse_detail']
{
    'no model_url': 'rr ',
}