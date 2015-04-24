# -*- coding: utf-8 -*-
"""
优信二手车需要更新的车源
"""

rule = {
    'name': '优信-更新规则',
    'domain': 'xin.com',
    'start_urls_category': 'usedcar',
    'model': 'product.CarSource',
    'class': 'CarSourceItem',
    'fields': {
        'price': {
            'xpath': (u'//div[@class="wan_1"]/em/text()',),
            'processors': ['first', 'price'],
        },
        'status': {
            'xpath': (
                # 下架
                u'not(contains(//body, "这个页面找不到啦"))',
                # 已售
                u'not(boolean(//div[@class="d-photo img-album"]/em))',
            ),
            'processors': ['first', 'strip', 'status'],
        },
    },
}
