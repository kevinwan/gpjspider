# -*- coding: utf-8 -*-
from gpjspider.utils.constants import SOURCE_TYPE_ODEALER
from .utils import *

item_rule = {
    "class": "UsedCarItem",
    "fields": {
        'title': {
            'xpath': (
                text(has_cls("tit", "/h1")),
            ),
            'required': True,
        },
        'dmodel': {
            'xpath': (
                text(cls('car-tit', '/p/a[5]')),
            ),
            'default': '%(title)s',
        },
        'meta': {
            'xpath': (
                '//meta[@name="description" or @name="Description"]/@content',
            ),
        },
        'year': {
            'xpath': (
                text(
                    cls('br', u'/span[contains(text(), "上牌时间")]/following-sibling::em')),
            ),
        },
        'month': {
            'xpath': (
                text(
                    cls('br', u'/span[contains(text(), "上牌时间")]/following-sibling::em')),
            ),
        },
        'mile': {
            'xpath': (
                text(
                    cls('br', u'/span[contains(text(), "行驶里程")]/following-sibling::em')),
                u'//div[@class="info"]/ul/li[2]/em//text()',
            ),
        },
        'volume': {
            'xpath': (
                text(
                    cls('br', u'/span[contains(text(), "排量")]/following-sibling::em')),
            ),
            'default': '%(title)s',
        },
        'phone': {
            'xpath': (
                text(with_cls('tel', '//span')),
            ),
            'after': ' ',
        },
        'color': {
            'xpath': (
                after_has(u"颜色"),
            ),
        },
        'control': {
            'xpath': (
                after_has(u"变速箱"),
            ),
            'default': '%(title)s',
        },
        'region': {
            'xpath': (
                text(cls("company", "/p[2]")),
            ),
        },
        'price': {
            'xpath': (
                text(cls("wan_1", "/em")),
            ),
        },
        'price_bn': {
            'xpath': (
                text(cls("wan_2", "/span/del")),
            ),
        },
        'brand_slug': {
            # 'xpath': (
            #     text(cls('car-tit', '/p/a[3]')),
            # text(cls("tit", '/h1')),
            # ),
            'default': '%(title)s',
        },
        'model_slug': {
            # 'xpath': [
            #     text(cls('car-tit', '/p/a[3]')),
            #     text(cls('car-tit', '/p/a[4]')),
            # text(cls("tit", '/h1')),
            # ],
            # 'xpath': (
            #     text(cls('car-tit', '/p/a[4]')),
            # text(cls("tit", '/h1')),
            # ),
            'default': '%(title)s',
            # 'processors': ['xin.model_slug'],
        },
        'model_url': {
            'xpath': (
                href(cls('car-tit', '/p/a[4]')),
            ),
            'format': True,
        },
        'city': {
            'xpath': (
                has(u'销售城市', '/../em', 'li/span'),
            ),
        },
        'description': {
            'xpath': (
                text(cls('test-txt', '/ul/li')),
            ),
            'processors': ['join'],
        },
        'imgurls': {
            'xpath': (
                attr(cls("carimg", "/div/img/"), 'data-original'),
                img(cls("carimg", "/div")),
            ),
            'processors': ['join'],
        },
        'mandatory_insurance': {
            'xpath': (
                after_has(u'保险到期时间', 'td', 'td'),
            ),
        },
        'company_name': {
            'xpath': (
                text(cls("newcompany", "/p")),
            ),
        },
        'company_url': {
            'xpath': (
                url(cls("newcompany")),
            ),
            'format': True,
        },
        'examine_insurance': {
            'xpath': (
                after_has(u'年检有效期'),
            ),
        },
        'transfer_owner': {
            'xpath': (
                after_has(u'过户次数'),
            ),
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
        'quality_service': {
            'xpath': (
                text(cls('test-txt', '/p/')),
                # u"//div[@class='day']//span[contains(text(), '退') or contains(text(), '修')  or contains(text(), '换' or contains(text(), '保'))]/text()",
                # u"//div[@class='msg']//li[contains(text(), '退') or contains(text(), '修') or contains(text(), '换') or contains(text(), '保')]/text()",
                # u"//div[@id='msgMore']/div[@class='msg']/ul/li[contains(text(), '退') or contains(text(), '修') or contains(text(), '换') or contains(text(), '保')]/text()",
                # img(cls("test-txt", '/')),
                # img(cls('day-pic', '/')),
            ),
            'processors': ['first', 'xin.quality_service'],
            'processors': ['join'],
        },
        'time': {
            'xpath': (
                after_has(u'检测时间', 'text()'),
                has(u'发布：'),
            ),
            # 'after': '：',
            'processors': ['first', 'after_colon'],
        },
        'is_certifield_car': {
            # 'xpath': (
            #     exists(cls('test-txt', '//img')),
            # img(cls('day-pic', '/')),
            # ),
            'default': "%(quality_service)s",
            'default_fail': False,
        },
        'source_type': {
            # 'xpath': (
            #     img(cls("test-txt", '/')),
            #     img(cls('day-pic', '/')),
            #     img(cls('day', '/')),
            # ),
            'default': SOURCE_TYPE_ODEALER,
            'default': '{item}',
            # 'default': '%(item)s',
            'processors': ['first', 'xin.source_type'],
            'processors': ['xin.source_type'],
        },
        'status': {
            'xpath': (
                u'//div[@class="d-photo img-album"]/em',
                u'//div[@class="error-wrap"]/div[@class="con"]/span[contains(text(),"页面找不到")]',
            ),
            'default': 'Y',
        }
    },
}

parse_rule = {
    "url": {
        "xpath": (
            url(has_cls('car-box', '//p')),
        ),
        "format": True,
        'contains': '/c/',
        "step": 'parse_detail',
        # 'max_pagenum': 50,
        # 'incr_pageno': 10,
    },
    'list_url': {
        'xpath': (
            url(cls('hot-city')),
        ),
        'format': True,
        'step': 'parse',
    },
    "next_page_url": {
        "xpath": (
            u'//a[contains(text(), "下一页")]/@data-page',
        ),
        "format": 'http://www.xin.com/quanguo/s/o2a10i{0}v1/',
        "step": 'parse',
    },
}

parse_list = {
    'url': {
        're': (
            r'/c/\d+\.html',
        ),
        'format': True,
        'step': 'parse_detail',
    },
    'next_page_url': {
        'xpath': (
            next_page1(),
        ),
        # 'excluded': ['javascript'],
        'regex': 'page=(\d+)',
        'format': True,
        'format': '%(url)s?page={0}',
        'format': '%(url)s',
        'replace': ['(page=\d+)', 'page={0}'],
        'step': 'parse_list',
        # 'dont_filter': False,
    },
}

rule = {
    'name': u'优信二手车',
    'domain': 'xin.com',
    'dealer': {
        'url': '%s?page=1',
    },
    'start_urls': [
        # 'http://www.xin.com/d/7679.html?page=1',
        'http://www.xin.com/quanguo/s/o2a10i1v1/',
        'http://www.xin.com/quanguo/s/o2a10i2v1/',
        'http://www.xin.com/quanguo/s/o2a10i3v1/',
        'http://www.xin.com/quanguo/s/o2a10i4v1/',
        'http://www.xin.com/quanguo/s/o2a10i6v1/',
        # 'http://www.xin.com/c/10424705.html',  # 5
        # 'http://www.xin.com/c/10353602.html',  # 5
        # 'http://www.xin.com/c/10254412.html',  # 2
        # 'http://www.xin.com/c/10354226.html',  # 3
        # 'http://www.xin.com/c/10354157.html',  # 2
        # 'http://www.xin.com/c/10358862.html',  # 3 Q
        # 'http://www.xin.com/c/10376527.html',  # 3
        # 'http://www.xin.com/c/10585041.html',  # 3
        # 'http://www.xin.com/c/10296987.html',  # offline
    ],
    'base_url': 'http://www.xin.com',
    'per_page': 20,
    'pages': 18489,

    'parse': parse_rule,
    'parse_list': parse_list,
    # 'parse': parse_list,

    'parse_detail': {
        "item": item_rule,
    }
}

fmt_rule_urls(rule)
# rule['parse'] = rule['parse_detail']
