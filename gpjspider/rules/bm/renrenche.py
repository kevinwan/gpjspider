# -*- coding: utf-8 -*-

rule = {
    # ==========================================================================
    # config 基本配置
    # ==========================================================================
    'name': u'brand_model.renrenche',
    'domain': 'renrenche.com',
    # start_urls  或者 start_url_template只能设置其一，
    # start_url_function 配合 start_url_template一起用
    # start_url_function 必须返回一个生成器
    'start_urls': [
        'http://www.renrenche.com/index.php?d=api&c=car_metainfo&m=index&type=get_brands',
    ],

    # ==========================================================================
    # parse 默认步骤
    # ==========================================================================
    'parse': {
        'items': {
            'class': 'BrandModelItem',
            'json': '-data',
            'fields': {
                'url': {
                    'key': 'brand_id',
                    'format': u'http://www.renrenche.com/index.php?d=api&c=car_metainfo&m=index&type=get_series_by_brand_id&brand_id={0}',
                },
                'name': {
                    'key': 'brand_name',
                    'required': True,
                },
                'slug': {
                    'key': 'brand_id',
                    'required': True,
                },
            },
            'teardown': 'renrenche.setup_brand',
        },
        'url': {
            'json': '-data$#$|ALL$#$-brand_id',
            'format': u'http://www.renrenche.com/index.php?d=api&c=car_metainfo&m=index&type=get_series_by_brand_id&brand_id={0}',
            'step': 'parse_list',
        },
    },
    # ==========================================================================
    # parse_list 列表页步骤
    # ==========================================================================
    'parse_list': {
        'items': {
            'class': 'BrandModelItem',
            'json': '-data',
            'fields': {
                'name': {
                    'key': 'series_name',
                    'required': True,
                },
                'slug': {
                    'key': 'series_id',
                    'required': True,
                },
                'parent': {
                    'json': '-brand_id',
                    'processors': ['renrenche.get_model_parent'],
                    'required': True,
                },
            }
        },
    },
}
