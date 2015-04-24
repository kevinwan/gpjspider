# -*- coding: utf-8 -*-
"""
好车无忧需要更新的车源
"""

rule = {
    'name': '好车无忧-更新规则',
    'domain': 'haoche51.com',
    'start_urls_category': 'usedcar',
    'model': 'product.CarSource',
    'class': 'CarSourceItem',
    'fields': {
        'price': {
            'xpath': ('//div[@class="car-quotation"]/strong/text()',),
            'processors': ['first', 'strip', 'price'],
        },
        'status': {
            'xpath': (
                u'not(contains(//body, "页面找不到了"))',  # 下架
                u'not(contains(//body, "车辆已成交"))',  # 已售
            ),
            'processors': ['first', 'strip', 'status'],
        },
    },
}
