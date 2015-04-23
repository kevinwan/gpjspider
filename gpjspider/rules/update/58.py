# -*- coding: utf-8 -*-
"""
58二手车需要更新的车源


func(response, self, *args, **kwargs)
"""

rule = {
    #==========================================================================
    #  基本配置
    #==========================================================================
    'name': '58二手车-更新规则',
    'domain': '58.com',
    'start_urls_category': 'usedcar',
    'model': 'product.CarSource',
    'class': 'CarSourceItem',
    'fields': {
        'price': {
            'xpath': ('//span[@class="font_jiage"]/text()',),
            'processors': ['first', 'strip', 'price'],
        },
        'status': {
            'function': {
                'name': 'status_58_car'
            },
        },
    },
}
