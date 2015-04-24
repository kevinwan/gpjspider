# -*- coding: utf-8 -*-
"""
赶集好车需要更新的车源
"""

rule = {
    'name': '赶集好车-更新规则',
    'domain': 'haoche.ganji.com',
    'start_urls_category': 'usedcar',
    'model': 'product.CarSource',
    'class': 'CarSourceItem',
    'fields': {
        'price': {
            'xpath': ('//b[@class="f30 numtype"]/text()',),
            'processors': ['first', 'strip', 'price'],
        },
        'status': {
            'xpath': (
                u'not(contains(//body, "帖子不存在"))',  # 下架
                u'not(contains(//p[@class="stipul-p"]/a/text(), "已售"))',  # 已售
            ),
            'processors': ['first', 'strip', 'status'],
        },
    },
}
