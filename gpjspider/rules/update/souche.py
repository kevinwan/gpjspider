# -*- coding: utf-8 -*-
"""
大搜车需要更新的车源
"""

rule = {
    'name': '大搜车-更新规则',
    'domain': 'souche.com',
    'start_urls_category': 'usedcar',
    'model': 'product.CarSource',
    'class': 'CarSourceItem',
    'fields': {
        'price': {
            'xpath': (
                '//div[@class="detail_price_left clearfix"]/em/text()',
            ),
            'processors': ['first', 'strip', 'price'],
        },
        'status': {
            'xpath': (
                # 下架
                u'not(boolean(//div[@id="pageError"]))',
                # 已售
                u'not(contains(//ins[@class="detail-no"]/text(), "已售"))',
            ),
            'processors': ['first', 'strip', 'status'],
        },
    },
}
