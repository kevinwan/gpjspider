# -*- coding: utf-8 -*-
from gpjspider.processors import renrenche
from copy import copy


def get_brand_urls(response, url_rule, spider):
    request = url_rule.get('request')
    urls = []
    for bid, name in renrenche.BRANDS.items():
        req = copy(request)
        req['url'] %= (bid, )
        urls.append(req)
    # spider.log(u'urls is: {0}'.format(urls))
    return urls

rule = {
    # ==========================================================================
    # config 基本配置
    # ==========================================================================
    'name': u'brand_model.ganjihaoche',
    'domain': 'haoche.ganji.com',
    # start_urls  或者 start_url_template只能设置其一，
    # start_url_function 配合 start_url_template一起用
    # start_url_function 必须返回一个生成器
    'start_urls': [
        'http://haoche.ganji.com/cd/sell/',
    ],

    # ==========================================================================
    # parse 默认步骤
    # ==========================================================================
    'parse': {
        'items': {
            'class': 'BrandModelItem',
            'xpath': '//input[@class="auto_select" and @data-role="minorShow"]/@data-source',
            'is_json': True,
            'fields': {
                'name': {
                    'key': 'text',
                    'required': True,
                },
                'slug': {
                    'key': 'id',
                    'required': True,
                },
            },
            'teardown': 'renrenche.setup_brand',
        },
        'url': {
            'function': get_brand_urls,
            'request': {
                'url': u'http://www.ganji.com/zq_haoche/?act=getTag&minorCategoryId=%s',
                'meta': {
                    'use_curl': True
                }
            },
            'step': 'parse_list',
        },
    },
    # ==========================================================================
    # parse_list 列表页步骤
    # ==========================================================================
    'parse_list': {
        'items': {
            'class': 'BrandModelItem',
            'json': 'ALL',
            'fields': {
                'name': {
                    'key': 'text',
                    'required': True,
                },
                'slug': {
                    'key': 'id',
                    'required': True,
                },
                'parent': {
                    'arg': 'minorCategoryId',
                    'processors': ['renrenche.get_model_parent'],
                    # TODO: add global support
                    # 'global': True,
                    'required': True,
                },
            }
        },
    },
}
