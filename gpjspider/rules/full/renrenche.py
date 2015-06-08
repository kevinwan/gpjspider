# -*- coding: utf-8 -*-
rule = {
    'domain': 'renrenche.com',
    'start_urls': ['http://www.renrenche.com/cn/ershouche'],
    'name': u'\u4eba\u4eba\u8f66',
    'parse_detail': {
        'item': {
            'fields': {'city_slug': {}, 'control': {'xpath': (u'//*[contains(text(), "\u53d8\u901f\u7bb1")]/following-sibling::*/text()',), 'processors': ['last']}, 'quality_service': {'xpath': (u'//td[contains(text(), "\u670d\u52a1\u9879")]/following-sibling::td//td/text()[2]',), 'processors': ['join']}, 'description': {'xpath': ('//div[@class="main"]/div/p/text()',), 'processors': ['join']}, 'business_insurance': {'xpath': (u'//*[contains(text(), "\u5546\u4e1a\u9669")]/following-sibling::*/text()',)}, 'color': {'xpath': (u'//*[contains(text(), "\u989c\u8272")]/following-sibling::*/text()',)}, 'model_slug': {'default': '%(title)s', 'before': ' '}, 'price': {'xpath': ('//*[@id="car_price"]/@value',)}, 'is_certifield_car': {'default': True}, 'phone': {'default': '%(meta)s', 'after': u'\u8be6\u8be2'}, 'month': {'xpath': (u'//*[contains(text(), "\u4e0a\u724c")]/following-sibling::*/text()',), 'default': '%(meta)s'}, 'volume': {'default': '%(meta)s', 'regex': u'\u6392\u6c14\u91cf[^\uff1a]{,4}\uff1a([^;\\s]+)'}, 'source_type': {'default': 2}, 'meta': {'xpath': ('//meta[@name="description" or @name="Description"]/@content',), 'processors': ['first']}, 'invoice': {'xpath': (u'//*[contains(text(), "\u8d2d\u8f66\u53d1\u7968")]/following-sibling::*/text()',)}, 'year': {'xpath': (u'//*[contains(text(), "\u4e0a\u724c")]/following-sibling::*/text()', u'//*[@id="hidBuyCarDate"]/@value | //*[contains(text(), "\u4e0a\u724c")]/following-sibling::text()', u'//*[@id="car_firstregtime"]/@value')}, 'brand_slug': {'default': '%(title)s', 'before': ' '}, 'maintenance_record': {'xpath': (u'//*[contains(text(), "\u662f\u54264S\u5e97\u4fdd\u517b")]/following-sibling::*/text()',), 'processors': ['first', 'has_maintenance_record']}, 'car_application': {}, 'mandatory_insurance': {'xpath': (
                u'//*[contains(text(), "\u4ea4\u5f3a\u9669")]/following-sibling::*/text()',)}, 'city': {'xpath': (u'//*[contains(text(), "\u5f52\u5c5e\u5730")]/following-sibling::*/text()',)}, 'dmodel': {'default': '%(title)s', 'after': '-', 'processors': ['first']}, 'title': {'xpath': ('//*[@id="car_info"]/@value',), 'required': True, 'processors': ['first']}, 'region': {'xpath': ('//div[@class="text-block bottom-right"]/h3/text()', u'//*[@class="address"]/text()'), 'processors': ['first', 'renrenche.region']}, 'condition_level': {'xpath': ('//span[@class="desc"]/text()',), 'processors': ['renrenche.cond_level']}, 'contact': {'default': u'\u4eba\u4eba\u8f66\u5ba2\u670d'}, 'examine_insurance': {'xpath': (u'//*[contains(text(), "\u5e74\u68c0")]/following-sibling::*/text()',)}, 'transfer_owner': {'xpath': (u'//*[contains(text(), "\u8fc7\u6237\u6b21\u6570")]/following-sibling::*/text()',)}, 'company_url': {'default': 'http://www.renrenche.com/'}, 'company_name': {'default': u'\u4eba\u4eba\u8f66'}, 'mile': {'xpath': (u'//*[contains(text(), "\u4eea\u8868\u76d8")]/following-sibling::*/text()', u'//*[contains(text(), "\u884c\u9a76\u91cc\u7a0b") | contains(text(), "\u4e07\u516c\u91cc")]/text()')}, 'condition_detail': {'xpath': ('//span[@class="desc"]/text()',), 'processors': ['join']}, 'time': {'xpath': (u'//*[contains(text(), "\u68c0\u6d4b\u65f6\u95f4")]/text()', u'//*[contains(text(), "\u53d1\u5e03\u65f6\u95f4")]/text()', u'//*[contains(text(), "\u53d1\u5e03\u65f6\u95f4")]/following-sibling::*/text()'), 'processors': ['first', 'after_colon', 'gpjtime']}, 'price_bn': {'xpath': ('//*[@id="basic"]/div[2]/div/div/div[1]/ul[1]/li/text()', '//*[@id="newCarPriceG"]/@value')}, 'imgurls': {'xpath': ('//div[@class="container detail-gallery"]/div//img/@src', '//div[@class="detail-box-bg"]/img/@src'), 'processors': ['join']}, 'driving_license': {}
            },
            'class': 'UsedCarItem',
        },
    },
    'base_url': 'http://www.renrenche.com',
    'parse': {
        'url': {'xpath': ('//*[contains(@class,"list-item")]/a[@href]/@href',), 'step': 'parse_detail', 'contains': ['/cn/car'], 'format': 'http://www.renrenche.com{0}'},
        'next_page_url': {
            'xpath': ('//a[text()=">"]/@href',),
            'step': 'parse',
            'format': 'http://www.renrenche.com{0}',
            # 'incr_pageno': 3,
        }
    }
}
