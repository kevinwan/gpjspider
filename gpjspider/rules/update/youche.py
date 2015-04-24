# -*- coding: utf-8 -*-
"""
优车诚品需要更新的车源
"""

rule = {
    'name': '优车诚品-更新规则',
    'domain': 'youche.com',
    'start_urls_category': 'usedcar',
    'model': 'product.CarSource',
    'class': 'CarSourceItem',
    'fields': {
        'price': {
            'xpath': (
                '//div[@class="nowPrice"]/b[@class="b0"]/text()',
            ),
            'processors': ['first', 'strip', 'price'],
        },
        'status': {
            'xpath': (
                # 下架
                'not(contains(//body, "error"))',
                # 找不到已售标志
            ),
            'processors': ['first', 'strip', 'status'],
        },
    },
}
