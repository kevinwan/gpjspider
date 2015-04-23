# -*- coding: utf-8 -*-
"""
cheyipai二手车需要更新的车源
"""

rule = {
    'name': 'cheyipai二手车-更新规则',
    'domain': 'c.cheyipai.com',
    'start_urls_category': 'usedcar',
    'model': 'product.CarSource',
    'class': 'CarSourceItem',
    'fields': {
        'price': {
            'json': '-data$#$-goodsPrice',
            'processors': ['strip', 'gpjfloat'],
        },
        'status': {
            'json': '-bstatus$#$-code',
            'processors': ['first', 'cheyipai.status'],
            'default': True,
        },
    },
}
