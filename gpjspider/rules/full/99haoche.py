# -*- coding: utf-8 -*-
"""
99好车 优质二手车 规则
"""
from gpjspider.utils.constants import SOURCE_TYPE_SELLER


rule = {
    #==========================================================================
    #  基本配置
    #==========================================================================
    'name': u'优质二手车-99好车-规则',
    'domain': '99haoche.com',
    'start_urls': [
        'http://www.chunshuitang.com/nvxing/3.html',  # 女佣
        'http://www.chunshuitang.com/nanxing/150.html',  # 男用
        'http://www.chunshuitang.com/yanshi/224.html',   # 延时锻炼
        'http://www.chunshuitang.com/category/230.html',  # 助情缩阴
        'http://www.chunshuitang.com/anquantao/125.html',  # 安全套
        'http://www.chunshuitang.com/runhuaji/126.html',  # 润滑剂
        'http://www.chunshuitang.com/fushi/6.html',  # 情趣服饰
    ],

    #==========================================================================
    #  默认步骤  parse
    #==========================================================================
    'parse': {
        "url": {
            "xpath": ('//*[@id="listBox"]/dl/dt/a/@href',),
            'format': 'http://www.chunshuitang.com{0}',
            # 新 url 对应的解析函数
            "step": 'parse_detail',
            'update': True,
            'category': 'product'
        },
        "next_page_url": {
            "xpath": (
                '//a[@class="page_next page_pnone page_colorc06 "]/@href',
            ),
            "step": 'parse',
        },
    },
    #==========================================================================
    #  详情页步骤  parse_detail
    #==========================================================================
    'parse_detail': {
        "item": {
            "class": "UsedCarItem",
            "fields": {
                'title': {
                    'xpath': ('//h1[@class="L_l"]/text()',),
                    'processors': ['first', 'strip'],
                    'required': True,
                },
                'subtitle': {
                    'xpath': ('//h1[@class="L_l"]/span/text()',),
                    'processors': ['first', 'strip'],
                },
                # 面包屑分类
                'navs': {
                    'xpath': ('//div[@class="L_title color666"]/a/text()',),
                    'processors': ['first', 'strip'],
                },
                'price': {
                    'xpath': ('//dt[@class="L_l  colorc06b  "]/text()',),
                    'processors': ['first', 'strip', 'price'],
                },
                


        },
    },
}
