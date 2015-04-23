# -*- coding: utf-8 -*-
"""
renren二手车需要更新的车源
"""

rule = {
    'name': 'renren二手车-更新规则',
    'domain': 'renrenche.com',
    'start_urls_category': 'usedcar',
    'model': 'product.CarSource',
    'class': 'CarSourceItem',
    'fields': {
        'price': {
            'xpath': ('//p[@class="box-price"]/text()',),
            'processors': ['first', 'strip', 'price'],
        },
        'status': {
            'xpath': (
                u'not(contains(//body, "这个页面开车离开网站了"))',
                u'not(contains(//button[@id="sold_button"]/text(), "已售"))',
            ),
            'processors': ['first', 'status'],
            'default': True,
        },
    },
}
