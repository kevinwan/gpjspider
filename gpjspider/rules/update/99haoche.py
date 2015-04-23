# -*- coding: utf-8 -*-
"""
99haoche二手车需要更新的车源
"""

rule = {
    'name': '99haoche二手车-更新规则',
    'domain': '99haoche.com',
    'start_urls_category': 'usedcar',
    'model': 'product.CarSource',
    'class': 'CarSourceItem',
    'fields': {
        'price': {
            'xpath': (
                '//p[@class="market-price"]/span[@class="str"]/text()',
            ),
            'processors': ['first', 'strip', 'price'],
        },
        'status': {
            'xpath': (
                u'not(contains(//body, "很抱歉，您访问的车辆已下架"))',  # 下架
                u'not(boolean(//div[@class="sold-out clearfix"]))',  # 已售
            ),
            'processors': ['first', 'status'],
            'default': True,
        },
    },
}
